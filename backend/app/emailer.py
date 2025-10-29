import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
REMINDER_MODE = os.getenv("EMAIL_MODE", "log")

def send_email(recipient_email: str, subject: str, body: str):
    print("Send email working")
    if REMINDER_MODE == "log":
        # internship-friendly: just log
        print(f"[{datetime.utcnow().isoformat()}] EMAIL to {recipient_email} | {subject}\n{body}\n")
        return True
    if REMINDER_MODE == "email":
        print("Email section working correctly")
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        SMTP_SERVER = os.getenv("SMTP_SERVER")
        SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
        SMTP_USER = os.getenv("SMTP_USER")
        SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
        EMAIL_FROM = os.getenv("SMTP_USER")
        print(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD")[:5])

        if not all([SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM]):
            print("[ERROR] SMTP configuration incomplete.")
            return False

        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(EMAIL_FROM, recipient_email, msg.as_string())
            print(f"[{datetime.utcnow().isoformat()}] EMAIL SENT to {recipient_email}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
            return False
    # If you configure SMTP, add smtplib sending here (not included for brevity)
    return False
