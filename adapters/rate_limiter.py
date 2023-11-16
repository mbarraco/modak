import abc
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from model import Notification

from . import NotificationConfigRepository


class AbstractRateLimiter(abc.ABC):
    @abc.abstractclassmethod
    def shall_pass(notification: Notification) -> bool:
        raise NotImplementedError


class SqlRateLimiter(AbstractRateLimiter):
    def __init__(self, session: Session, repo: NotificationConfigRepository):
        self.session = session
        self.repo = repo

    def shall_pass(self, notification: Notification) -> bool:
        config = self.repo.find_by_type(notification.notification_type)
        if not config:
            return True

        time_limit = datetime.utcnow() - timedelta(
            days=config.days, hours=config.hours, minutes=config.minutes
        )
        recent_notifications_count = (
            self.session.query(Notification)
            .filter(
                Notification.notification_type == notification.notification_type,
                Notification.last_updated > time_limit,
            )
            .count()
        )

        return recent_notifications_count < config.quota
