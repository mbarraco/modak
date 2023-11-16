import abc
from adapters.email_server import EmailServer
from domain.model import Notification


class AbstractEmailSender(abc.ABC):
    @abc.abstractclassmethod
    def send_email(content: Notification):
        raise NotImplementedError


class EmailSender(AbstractEmailSender):
    def __init__(self, server: EmailServer):
        self.server = server

    def send_email(self, notification: Notification) -> dict[str, tuple[int, bytes]]:
        return self.server.send_email(notification)
