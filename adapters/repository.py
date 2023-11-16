import abc

from sqlalchemy.orm import Session

from model import Notification, NotificationConfig


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self, session: Session):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, notification: Notification):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError


class NotificationRepository:
    model = Notification

    def __init__(self, session: Session):
        self.session = session

    def add(self, notification: Notification):
        self.session.add(notification)

    def list(self):
        return self.session.query(self.model).all()


class NotificationConfigRepository(AbstractRepository):
    model = NotificationConfig

    def __init__(self, session: Session):
        self.session = session

    def add(self, notification_config: NotificationConfig):
        self.session.add(notification_config)

    def list(self):
        return self.session.query(self.model).all()

    def find_by_type(self, notification_type):
        return (
            self.session.query(self.model)
            .filter_by(notification_type=notification_type)
            .one_or_none()
        )
