  # process_replies.py
import imaplib
import email
from email.message import EmailMessage
import smtplib
import os
from intent_detector import detect_intent
from auto_reply import generate_reply
from dotenv import load_dotenv
# ==============================
# PROCESS REPLIES FUNCTION
# ==============================
def process_replies_function():
    # load environment variables inside the function
    
    load_dotenv()  # only for local testing

    EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    if not EMAIL_ACCOUNT or not APP_PASSWORD:
        print("❌ Missing EMAIL_ACCOUNT or APP_PASSWORD")
        return

    """
    Reads unread emails, detects intent, and sends automated HTML replies.

    Parameters:
    - email_account: your email used for sending/receiving
    - app_password: app password for the email
    """

    # ------------------------------
    # Create logs folder
    # ------------------------------
    os.makedirs("logs", exist_ok=True)

    # ------------------------------
    # Connect SMTP (send emails)
    # ------------------------------
    try:
        smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp.login(EMAIL_ACCOUNT, APP_PASSWORD)
        print("✅ Logged into SMTP for sending replies")
    except Exception as e:
        print(f"❌ SMTP login failed: {e}")
        return

    # ------------------------------
    # Connect IMAP (read emails)
    # ------------------------------
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
        mail.select("inbox")
        print("📥 Connected to inbox via IMAP")
    except Exception as e:
        print(f"❌ IMAP login failed: {e}")
        smtp.quit()
        return

    # ------------------------------
    # Search unread emails
    # ------------------------------
    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()
    print(f"📥 Unread emails: {len(email_ids)}")

    # ------------------------------
    # HTML auto-reply template builder
    # ------------------------------
    def build_html_reply(student_name, intent, reply_message):
     return f"""
<!DOCTYPE html>
<html>
  <body style="margin:0; padding:0; background-color:#f4f6f9; font-family: Arial, Helvetica, sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f9; padding:20px;">
      <tr>
        <td align="center">

          <table width="600" cellpadding="0" cellspacing="0"
                 style="background-color:#ffffff; border-radius:8px;
                        box-shadow:0 0 10px rgba(0,0,0,0.08); overflow:hidden;">

            <!-- ================= HEADER ================= -->
            <tr>
              <td style="padding:20px; border-bottom:1px solid #e5e5e5;">
                <table width="100%">
                  <tr>
                    <!-- LOGO -->
                    <td align="left">
                      <img src="https://www.webearl.com/img/logo.png"
                           alt="School Logo"
                           style="max-height:30px;">
                    </td>

                    <!-- SCHOOL DETAILS -->
                    <td align="right"
                        style="font-size:14px; color:#7f8c8d; line-height:1.4;">
                      <strong>ABC Public School</strong><br>
                      Accounts Department<br>
                      Contact: +91 9898989898<br>
                      Website: https://www.webearl.com
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- ================= TITLE ================= -->
            <tr>
              <td align="center" style="padding:20px;">
                <h1 style="margin:0; font-size:24px; color:#2c3e50;">
                  Fee Communication – Auto Reply
                </h1>
              </td>
            </tr>

            <!-- ================= BODY ================= -->
            <tr>
              <td style="padding:0 30px 20px;
                         font-size:15px;
                         color:#2c3e50;
                         line-height:1.6;">

                <p>Dear Parent of <strong>{student_name}</strong>,</p>

                <p>
                  Your message has been received and reviewed by our Accounts Department.
                </p>

                <table width="100%" cellpadding="10" cellspacing="0"
                       style="border:1px solid #e0e0e0;
                              border-radius:6px;
                              margin:15px 0;
                              background-color:#f9f9f9;">

                  <tr>
                    <td><strong>Detected Request Type</strong></td>
                    <td style="font-weight:bold; color:#c0392b;">
                      {intent}
                    </td>
                  </tr>

                </table>

                <table width="100%" cellpadding="12" cellspacing="0"
                       style="border:1px solid #e0e0e0;
                              border-radius:6px;
                              margin:15px 0;">
                  <tr>
                    <td style="font-size:15px; line-height:1.6; white-space:pre-line;">
                      {reply_message}
                    </td>
                  </tr>
                </table>

                <p>
                  If you have any further questions, feel free to contact the Accounts Office.
                </p>

                <p style="margin-top:20px;">
                  Regards,<br>
                  <strong>ABC Public School</strong><br>
                  Accounts Department
                </p>

              </td>
            </tr>

            <!-- ================= FOOTER ================= -->
            <tr>
              <td align="center"
                  style="padding:15px;
                         font-size:12px;
                         color:#95a5a6;
                         background-color:#fafafa;
                         border-top:1px solid #e5e5e5;">
                This is an automated email. Please do not reply.
              </td>
            </tr>

          </table>

        </td>
      </tr>
    </table>

  </body>
</html>
"""
    # ------------------------------
    # Loop through unread emails
    # ------------------------------
    for email_id in email_ids:
        try:
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Get sender email
            from_email = email.utils.parseaddr(msg.get("From"))[1]

            # Get email body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            # Detect intent
            intent = detect_intent(body)
            print(f"Detected Intent from {from_email}: {intent}")

            # Generate reply text
            student_name = "Student"  # can be mapped from Excel if needed
            reply_text = generate_reply(intent, student_name)

            # Build HTML email
            html_content = build_html_reply(student_name, intent, reply_text)

            # Create email
            reply = EmailMessage()
            reply["From"] = EMAIL_ACCOUNT
            reply["To"] = from_email
            reply["Subject"] = "Re: Fee Communication"
            reply.set_content("Your email client does not support HTML.")
            reply.add_alternative(html_content, subtype="html")

            # Send email
            smtp.send_message(reply)

            # Log success
            with open("logs/replies.log", "a") as f:
                f.write(f"REPLIED TO: {from_email} | INTENT: {intent}\n")

            print(f"✅ Auto-replied to {from_email}")

        except Exception as e:
            print(f"❌ Failed to process email: {e}")
            with open("logs/replies.log", "a") as f:
                f.write(f"FAILED TO PROCESS: {from_email if 'from_email' in locals() else 'UNKNOWN'} | {e}\n")

    # ------------------------------
    # Close connections
    # ------------------------------
    smtp.quit()
    mail.logout()
    print("🎉 All replies processed and logged successfully!")
