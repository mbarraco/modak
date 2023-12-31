import smtplib
from email.message import EmailMessage

from domain.model import Notification


class EmailServer:
    def __init__(self, smtp_server, smtp_port):
        self.connection = smtplib.SMTP(smtp_server, smtp_port)

    def send_email(self, email_content: Notification) -> dict[str, tuple[int, bytes]]:
        msg = EmailMessage()
        msg["Subject"] = email_content.subject
        msg["From"] = email_content.from_email
        msg["To"] = email_content.to_email
        msg.set_content(email_content.body)
        return self.connection.send_message(msg)

    def close(self):
        self.connection.quit()
