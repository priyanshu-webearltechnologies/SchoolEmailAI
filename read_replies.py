import imaplib
import email
from email.header import decode_header
import os


# ==============================
# GMAIL CONFIGURATION
# ==============================
EMAIL_ACCOUNT="priyanshu.webearltechnologies@gmail.com"
APP_PASSWORD="leruaimpymrdighh"

# ==============================
# CONNECT TO GMAIL IMAP
# ==============================
try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
    print("✅ Logged into Gmail IMAP")

except Exception as e:
    print("❌ IMAP login failed:", e)
    exit()

# ==============================
# SELECT INBOX
# ==============================
mail.select("inbox")

# ==============================
# SEARCH FOR UNREAD EMAILS
# ==============================
status, messages = mail.search(None, "UNSEEN")

email_ids = messages[0].split()
print(f"📥 Unread emails found: {len(email_ids)}\n")

# ==============================
# READ EACH UNREAD EMAIL
# ==============================
for email_id in email_ids:
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    raw_email = msg_data[0][1]

    msg = email.message_from_bytes(raw_email)

    # Decode subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8")

    from_email = msg.get("From")

    print("📨 New Reply Received")
    print(f"From    : {from_email}")
    print(f"Subject : {subject}")

    # ==============================
    # READ EMAIL BODY
    # ==============================
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode()
                print("Message:")
                print(body)
                break
    else:
        body = msg.get_payload(decode=True).decode()
        print("Message:")
        print(body)

    print("-" * 60)

# ==============================
# LOGOUT
# ==============================
mail.logout()
