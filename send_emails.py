# send_emails.py
import pandas as pd
import smtplib
from email.message import EmailMessage
import time
import os


# ==============================
# SEND EMAILS FUNCTION
# ==============================
def send_emails_function(
    excel_file: str = "student_demo.xlsx",
    template_file: str = "email_template.html",
    delay: int = 5
):
    """
    Sends bulk emails to students based on Excel file and HTML template.
    
    Parameters:
    - excel_file: path to the Excel file containing student data
    - template_file: path to the HTML email template
    - delay: delay in seconds between sending emails
    """
    
    # ------------------------------
    # Create logs folder
    # ------------------------------
    os.makedirs("logs", exist_ok=True)

    # ------------------------------
    # Load environment variables
    # ------------------------------
    EMAIL_ACCOUNT="priyanshu.webearltechnologies@gmail.com"
    APP_PASSWORD="leruaimpymrdighh"
    if not EMAIL_ACCOUNT or not APP_PASSWORD:
        print("❌ Missing EMAIL_ACCOUNT or APP_PASSWORD ")
        return

    # ------------------------------
    # Load HTML template
    # ------------------------------
    try:
        with open(template_file, "r", encoding="utf-8") as f:
            email_template = f.read()
    except Exception as e:
        print(f"❌ Failed to read template: {e}")
        return

    # ------------------------------
    # Load Excel file
    # ------------------------------
    try:
        data = pd.read_excel(excel_file)
    except Exception as e:
        print(f"❌ Failed to read Excel file: {e}")
        return

    print(f"📄 Excel file loaded successfully ({len(data)} emails)")

    # ------------------------------
    # Connect to Gmail SMTP
    # ------------------------------
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_ACCOUNT, APP_PASSWORD)
        print("✅ Logged into Gmail SMTP")
    except Exception as e:
        print(f"❌ SMTP login failed: {e}")
        return

    # ------------------------------
    # Loop through Excel and send emails
    # ------------------------------
    for index, row in data.iterrows():
        receiver_email = row.get("Student Emails", "UNKNOWN")
        try:
            first_name = row.get("First Name", "")
            last_name = row.get("Last Name", "")
            student_class = row.get("Class", "")
            roll_no = row.get("Roll No.", "")
            fee_amount = row.get("Fee Amount", "")
            
            # Handle date safely
            due_date_raw = row.get("Due Dates ", "")
            try:
                due_date = due_date_raw.strftime("%d/%m/%Y")
            except AttributeError:
                due_date = str(due_date_raw)

            full_name = f"{first_name} {last_name}"

            # Prepare HTML body
            html_body = email_template.replace("{{FULL_NAME}}", full_name)
            html_body = html_body.replace("{{CLASS}}", str(student_class))
            html_body = html_body.replace("{{ROLL_NO}}", str(roll_no))
            html_body = html_body.replace("{{FEE_AMOUNT}}", str(fee_amount))
            html_body = html_body.replace("{{DUE_DATE}}", due_date)

            # Create email
            msg = EmailMessage()
            msg["From"] = EMAIL_ACCOUNT
            msg["To"] = receiver_email
            msg["Subject"] = "Pending School Fee Reminder"
            msg.set_content(html_body, subtype="html")

            # Send email
            server.send_message(msg)

            # Log success
            with open("logs/sent_emails.log", "a") as f:
                f.write(f"SUCCESS: {receiver_email}\n")

            print(f"✅ Email sent to: {receiver_email}")
            time.sleep(delay)

        except Exception as e:
            print(f"❌ Failed to send email to {receiver_email}: {e}")
            with open("logs/failed_emails.log", "a") as f:
                f.write(f"FAILED: {receiver_email} | {e}\n")

    # ------------------------------
    # Close SMTP connection
    # ------------------------------
    server.quit()
    print("🎉 All emails processed successfully!")
