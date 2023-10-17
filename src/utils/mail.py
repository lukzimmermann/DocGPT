from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from secrets import token_urlsafe
import smtplib, ssl
from dotenv import load_dotenv

load_dotenv()

def send_mail(receiver_email: str, subject: str, body: str):
    smtp_server = os.getenv("MAIL_SERVER")
    port = os.getenv("MAIL_PORT")
    sender_email = os.getenv("MAIL_SENDER")
    password = os.getenv("MAIL_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body,'html'))

    text = msg.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        #server.set_debuglevel(1)
        server.ehlo
        server.sendmail(sender_email, [receiver_email], text)
        server.quit()


