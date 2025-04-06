import os
import shutil
import smtplib
from email.message import EmailMessage
import mimetypes
from getpass import getpass


def rename_files_in_directory(folder_path, prefix, start_number=1):
    if not os.path.isdir(folder_path):
        print("❌ Invalid folder path.")
        return

    files = os.listdir(folder_path)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    files.sort()

    for i, filename in enumerate(files, start=start_number):
        ext = os.path.splitext(filename)[1]
        new_name = f"{prefix}_{i}{ext}"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))
    print(f"✅ Renamed {len(files)} files.")


def optimize_directory(folder_path, sort_files=False):
    if not os.path.isdir(folder_path):
        print("❌ Invalid folder path.")
        return

    # Remove empty folders
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for d in dirs:
            full_path = os.path.join(root, d)
            if not os.listdir(full_path):
                os.rmdir(full_path)
                print(f"🗑 Removed empty folder: {full_path}")

    # Sort files into subfolders by extension
    if sort_files:
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            if os.path.isfile(full_path):
                ext = os.path.splitext(filename)[1][1:].lower()
                if not ext:
                    ext = "unknown"
                ext_folder = os.path.join(folder_path, ext)
                os.makedirs(ext_folder, exist_ok=True)
                shutil.move(full_path, os.path.join(ext_folder, filename))
        print("📁 Sorted files by extension.")

    print("✅ Directory optimized.")


def send_email(sender_email, password, receiver_email, subject, body, attachments=[]):
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(body)

    for path in attachments:
        if not os.path.isfile(path):
            continue
        mime_type, _ = mimetypes.guess_type(path)
        mime_type, mime_subtype = mime_type.split('/') if mime_type else ('application', 'octet-stream')

        with open(path, 'rb') as f:
            msg.add_attachment(f.read(),
                               maintype=mime_type,
                               subtype=mime_subtype,
                               filename=os.path.basename(path))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, password)
            smtp.send_message(msg)
            print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


def main():
    while True:
        print("\n=== Task Automation Menu ===")
        print("1. Rename files in folder")
        print("2. Optimize directory (clean & sort)")
        print("3. Send automated email")
        print("4. Exit")
        choice = input("Select an option (1-4): ")

        if choice == '1':
            folder = input("Enter folder path: ")
            prefix = input("Enter filename prefix: ")
            start = input("Start numbering from (default 1): ") or "1"
            rename_files_in_directory(folder, prefix, int(start))
        elif choice == '2':
            folder = input("Enter folder path to optimize: ")
            sort = input("Sort files into subfolders by type? (y/n): ").lower() == 'y'
            optimize_directory(folder, sort)
        elif choice == '3':
            sender = input("Your email (Gmail): ")
            password = getpass("App Password (Gmail app-specific password recommended): ")
            receiver = input("Receiver email: ")
            subject = input("Email subject: ")
            body = input("Email body: ")
            attach = input("Attach files? (comma-separated full paths, or leave blank): ")
            attachment_paths = [a.strip() for a in attach.split(',')] if attach else []
            send_email(sender, password, receiver, subject, body, attachment_paths)
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()
