import os
from email.message import EmailMessage
import smtplib

def send_email(receiver_email,otp):

    if not receiver_email or not otp:
        return {"status":"error","message" :"Missing required fields"}

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")  
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        return {"status":"error","message" :"SMTP credentials are missing"}

    SENDER_EMAIL = smtp_user
    try:
        msg = EmailMessage()
        msg.set_content(f'Your OTP code is {otp}. It is valid for 10 minutes.')
        msg['Subject'] = 'Your OTP Code'
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email

        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, receiver_email, msg.as_string())
        return {"status":"success","message" :"Email sent successfully"}

    except Exception as e:
        print("Error:", str(e))
        return {"status":"error","message" :str(e)}
