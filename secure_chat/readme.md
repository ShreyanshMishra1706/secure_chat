# Secure Chat Application

## Prerequisites
Ensure you have **Python 3.11.xx** installed. If not, uninstall your current Python version and install **3.11.xx** before proceeding.

## Setup Instructions

1. **Create a Project Folder**
   ```sh
   mkdir Chat_App
   cd Chat_App
   ```
2. **Set Up a Virtual Environment**
   ```sh
   python -m venv env
   ```
3. **Unzip the provided file inside `Chat_App`**
4. **Open the Project in VS Code**
5. **Select the Python Interpreter**
   - Choose `venv:env` as the interpreter.
6. **Open a New Terminal**
   - Ensure it is **Command Prompt (cmd)**, not PowerShell or any other terminal.
   - If needed, switch by clicking the `+` symbol and selecting `cmd`.
7. **Navigate to the `secure_chat` Directory**
   ```sh
   cd secure_chat
   ```
8. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
9. **Run the Server**
   ```sh
   daphne secure_chat.asgi:application
   ```
10. The server will start at `127.0.0.1:8000`.
    - Open this address in a browser to access the application.

---

## Admin Credentials
- **Admin Panel:** [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
- **Username:** `admin`
- **Password:** `admin`

## User Credentials
- **Usernames:** Refer to the provided image for a list of available usernames.
- **Password for all users:** `pass@123`

---

## Features to Test

✅ **User Registration**
   - Newly registered users should appear in the admin panel.

✅ **Login/Logout**

✅ **Chat Functionality**
   - Ensure both users are in the same chat room.
   - **Notification system is not implemented (Time-bounded testing required).**
   - **Chatting must be done in either:**
     - Two separate browsers
     - One in regular mode and another in incognito mode
   - **Two tabs in the same browser will not work.**

✅ **Static Pages**
   - Home page, About page, and other available static pages.

---

### Enjoy Testing! 🚀
