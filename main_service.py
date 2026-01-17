import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SEND_EMAIL_SCRIPT = os.path.join(BASE_DIR, "send_emails.py")
PROCESS_REPLIES_SCRIPT = os.path.join(BASE_DIR, "process_replies.py")

def run_script(script_path):
    try:
        print(f"STARTING: {os.path.basename(script_path)}")
        subprocess.run([sys.executable, script_path], check=True)
        print(f"COMPLETED: {os.path.basename(script_path)}\n")
    except subprocess.CalledProcessError as e:
        print(f"ERROR in {os.path.basename(script_path)}:", e)

def run_full_workflow():
    print("\n===== FULL WORKFLOW STARTED =====")
    run_script(SEND_EMAIL_SCRIPT)
    run_script(PROCESS_REPLIES_SCRIPT)
    print("===== FULL WORKFLOW COMPLETED =====\n")

def show_scheduling_instructions():
    print("\n⏰ AUTOMATIC SCHEDULING SETUP (WINDOWS)")
    print("-------------------------------------")
    print("Follow these steps carefully:\n")
    print("1️⃣ Press Windows Key + R")
    print("2️⃣ Type: taskschd.msc")
    print("3️⃣ Press Enter\n")
    print("4️⃣ Click 'Create Basic Task'")
    print("5️⃣ Name it: School Email Automation\n")
    print("6️⃣ Choose trigger:")
    print("   • Daily (recommended)")
    print("   • Or Hourly\n")
    print("7️⃣ Action → Start a Program")
    print("8️⃣ Program/script:")
    print("   • Browse and select THIS application")
    print("     (or main_service.py / EXE)\n")
    print("9️⃣ Click Next → Finish\n")
    print("✅ Automation will now run automatically")
    print("   even if the app is closed.\n")
    print("⚠️ NOTE:")
    print("• Do this ONE TIME only")
    print("• Keep Excel file in the same folder\n")

def menu():
    while True:
        print("\n🏫 SCHOOL EMAIL AUTOMATION SYSTEM")
        print("--------------------------------")
        print("1️⃣ Send Fee Reminder Emails")
        print("2️⃣ Reply to Incoming Emails")
        print("3️⃣ Run Full Automation (Send + Reply)")
        print("4️⃣ Setup Automatic Scheduling")
        print("5️⃣ Exit\n")

        choice = input("Select an option (1/2/3/4/5): ")

        if choice == "1":
            print("\n📤 Sending Fee Reminder Emails...\n")
            run_script(SEND_EMAIL_SCRIPT)

        elif choice == "2":
            print("\n📥 Processing & Replying to Emails...\n")
            run_script(PROCESS_REPLIES_SCRIPT)

        elif choice == "3":
            run_full_workflow()

        elif choice == "4":
            show_scheduling_instructions()

        elif choice == "5":
            print("👋 Exiting system...")
            break

        else:
            print("❌ Invalid option. Please try again.\n")

if __name__ == "__main__":
    menu()
