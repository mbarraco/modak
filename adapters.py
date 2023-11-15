import abc

from sqlalchemy.orm import Session

from model import Notification
from email_server import EmailServer


class AbstractEmailSender(abc.ABC):
    @abc.abstractclassmethod
    def send_email(content: Notification):
        raise NotImplementedError


class EmailSender(AbstractEmailSender):
    def __init__(self, server: EmailServer):
        self.server = server

    def send_email(self, notification: Notification) -> dict[str, tuple[int, bytes]]:
        return self.server.send_email(notification)


class NotificationRepository(abc.ABC):

    model = Notification

    def __init__(self, session: Session):
        self.session = session

    def add(self, notification: Notification):
        self.session.add(notification)

    def update(self, notification_id: int, **updates):
        notification = self.session.query(Notification).filter_by(id=notification_id).one()
        for key, value in updates.items():
            setattr(notification, key, value)

    def list(self):
        return self.session.query(self.model).all()