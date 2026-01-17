import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import runpy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SEND_EMAIL_SCRIPT = os.path.join(BASE_DIR, "send_emails.py")
PROCESS_REPLIES_SCRIPT = os.path.join(BASE_DIR, "process_replies.py")

# ==============================
# CORE EXECUTION
# ==============================s

def run_script(script_path):
    try:
        if getattr(sys, 'frozen', False):
            runpy.run_path(script_path, run_name="__main__")
        else:
            subprocess.run([sys.executable, script_path], check=True)

        messagebox.showinfo(
            "Success",
            f"{os.path.basename(script_path)} completed successfully"
        )
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Error running {os.path.basename(script_path)}\n{e}"
        )

def send_emails():
    run_script(SEND_EMAIL_SCRIPT)

def reply_emails():
    run_script(PROCESS_REPLIES_SCRIPT)

def run_full():
    try:
        if getattr(sys, 'frozen', False):
            runpy.run_path(SEND_EMAIL_SCRIPT, run_name="__main__")
            runpy.run_path(PROCESS_REPLIES_SCRIPT, run_name="__main__")
        else:
            subprocess.run([sys.executable, SEND_EMAIL_SCRIPT], check=True)
            subprocess.run([sys.executable, PROCESS_REPLIES_SCRIPT], check=True)

        messagebox.showinfo("Success", "Full workflow completed successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ==============================
# AUTOMATIC SCHEDULING
# ==============================

def setup_scheduler():
    instructions = """
AUTOMATIC SCHEDULING SETUP (WINDOWS)

Follow these steps carefully:

1️⃣ Press Windows Key + R
2️⃣ Type: taskschd.msc
3️⃣ Press Enter

4️⃣ Click "Create Basic Task"
5️⃣ Name it: School Email Automation

6️⃣ Choose trigger:
   • Daily (recommended)
   • Or Hourly

7️⃣ Action → Start a Program

8️⃣ Program/script:
   • Browse and select THIS application (.exe)

9️⃣ Click Next → Finish

✅ Automation will now run automatically
even if the app is closed.

⚠️ NOTE:
• Do this ONE TIME only
• Keep Excel file in same folder
"""

    messagebox.showinfo("Automatic Scheduling Instructions", instructions)


# ==============================
# GUI
# ==============================

app = tk.Tk()
app.title("School Email Automation System")
app.geometry("420x360")
app.resizable(False, False)

tk.Label(
    app,
    text="🏫 School Email Automation",
    font=("Arial", 16, "bold")
).pack(pady=15)

tk.Button(
    app,
    text="📤 Send Fee Reminder Emails",
    width=30,
    height=2,
    command=send_emails
).pack(pady=6)

tk.Button(
    app,
    text="📥 Reply to Incoming Emails",
    width=30,
    height=2,
    command=reply_emails
).pack(pady=6)

tk.Button(
    app,
    text="🔁 Run Full Automation",
    width=30,
    height=2,
    command=run_full
).pack(pady=6)

tk.Button(
    app,
    text="⏰ Setup Automatic Scheduling",
    width=30,
    height=2,
    command=setup_scheduler
).pack(pady=6)

tk.Button(
    app,
    text="❌ Exit",
    width=30,
    height=2,
    command=app.quit
).pack(pady=10)

app.mainloop()
