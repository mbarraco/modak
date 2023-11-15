from dataclasses import dataclass
from enum import Enum
import re


def is_valid_email(s: str) -> bool:
    exp = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.match(exp, s)


@dataclass(frozen=True)
class EmailContent:
    from_email: str
    body: str
    subject: str
    to_email: str

class NotificationType(Enum):
    SUPDATESUPDATE = 1
    DAILY_NEWS = 2
    PROJECT_INVITATIONS = 3

@dataclass(frozen=True)
class Notification:
    email_content: EmailContent
    type:  NotificationType

    def __post_init__(self):
        if not is_valid_email(self.email_content.to_email):
            raise ValueError(f"Invalid email address: {self.email_content.to_email}")
        if not is_valid_email(self.email_content.from_email):
            raise ValueError(f"Invalid email address: {self.email_content.to_email}")


