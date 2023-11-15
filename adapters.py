import abc
import smtplib
from email.mime.text import MIMEText

from model import Notification
from email_server import EmailServer


class AbstractEmailSender(abc.ABC):
    @abc.abstractclassmethod
    def send_email(content: Notification):
        raise NotImplementedError


class EmailSender(AbstractEmailSender):
    def __init__(self, server: EmailServer):
        self.server = server

    def send_email(self, content: Notification) -> dict[str, tuple[int, bytes]]:
        return self.server.send_email(content)
