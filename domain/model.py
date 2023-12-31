from datetime import datetime
from enum import Enum
import re


def _is_valid_email(s: str) -> bool:
    exp = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    return re.match(exp, s)


class Notification:
    def __init__(
        self,
        from_email: str,
        body: str,
        subject: str,
        to_email: str,
        notification_type: "NotificationType",
    ):
        self.from_email = from_email
        self.body = body
        self.subject = subject
        self.to_email = to_email
        self.notification_type = notification_type
        self.state = NotificationState.PENDING
        self.last_updated = datetime.utcnow()

        self._validate()

    def _validate(self) -> None:
        if not _is_valid_email(self.to_email):
            raise ValueError(f"Invalid email address: {self.to_email}")
        if not _is_valid_email(self.from_email):
            raise ValueError(f"Invalid email address: {self.from_email}")

    def mark_sent(self):
        self.state = NotificationState.SENT

    def mark_rejected(self):
        self.state = NotificationState.REJECTED

    def mark_updated(self):
        self.last_updated = datetime.utcnow()


class NotificationState(Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    REJECTED = "REJECTED"


class NotificationType(Enum):
    MARKETING = "MARKETING"
    NEWS = "NEWS"
    STATUS = "STATUS"


class NotificationConfig:
    def __init__(
        self,
        notification_type: NotificationType,
        seconds: int,
        quota: int,
    ):
        self.notification_type = notification_type
        self.seconds = seconds
        self.quota = quota

    @property
    def interval_in_seconds(self):
        return self.seconds
