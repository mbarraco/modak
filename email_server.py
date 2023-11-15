import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage



from model import EmailContent



class EmailServer:
    def __init__(self, smtp_server, smtp_port):
        self.connection = smtplib.SMTP(smtp_server, smtp_port)

    def send_email(self, email_content: EmailContent) -> dict[str, tuple[int, bytes]]:
        msg = EmailMessage()
        msg['Subject'] = email_content.subject
        msg['From'] = email_content.from_email
        msg['To'] = email_content.to_email
        msg.set_content(email_content.body)
        return self.connection.send_message(msg)


    def close(self):
        self.connection.quit()
