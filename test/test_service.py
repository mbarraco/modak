from sqlalchemy import text

import service.service as service
from adapters import (
    EmailSender,
    NotificationRepository,
    NotificationConfigRepository,
    SqlRateLimiter,
)
from domain.model import Notification, NotificationState, NotificationType
from .test_utils import count_emails, get_latest_email


def test_send_notification(email_server, session, create_notification):
    email_sender = EmailSender(email_server)
    repo = NotificationRepository(session)
    notification: Notification = create_notification(NotificationType.NEWS)
    rate_limiter = SqlRateLimiter(session, NotificationConfigRepository(session))
    service.send_notification(notification, email_sender, repo, rate_limiter)
    service.send_notification(notification, email_sender, repo, rate_limiter)

    latest_email = get_latest_email()
    assert notification.from_email == latest_email["Raw"]["From"]
    assert [notification.to_email] == latest_email["Raw"]["To"]
    assert notification.body == latest_email["Content"]["Body"]
    assert [notification.subject] == latest_email["Content"]["Headers"]["Subject"]


def test_do_send_email_saves_notification(email_server, session, create_notification):
    email_sender = EmailSender(email_server)
    repo = NotificationRepository(session)
    notification = create_notification(NotificationType.NEWS)
    rate_limiter = SqlRateLimiter(session, NotificationConfigRepository(session))
    service.send_notification(notification, email_sender, repo, rate_limiter)
    retrieved = repo.list()
    assert len(retrieved) == 1
    assert retrieved[0] == notification


def test_throttling_sql_rate_limiter(email_server, session, create_notification):
    session.execute(
        text(
            "INSERT INTO notification_configs (notification_type, days, hours, minutes, quota)"
            f" VALUES ('{NotificationType.NEWS.value}', 0, 0, 1, 1)"
        )
    )

    session.execute(
        text(
            "INSERT INTO notifications (from_email, to_email, subject, body, notification_type, state, last_updated)"
            f" VALUES ('from-1234@email.com', 'to-1234@email.com', 'Example Subject', 'Example body content', "
            f" '{NotificationType.NEWS.value}', '{NotificationState.SENT.value}', CURRENT_TIMESTAMP)"
        )
    )
    email_sender = EmailSender(email_server)
    repo = NotificationRepository(session)
    rate_limiter = SqlRateLimiter(session, NotificationConfigRepository(session))
    notification = create_notification(NotificationType.NEWS)
    service.send_notification(notification, email_sender, repo, rate_limiter)
    retrieved = repo.list()
    assert len(retrieved) == 2
    assert retrieved[0].state == NotificationState.SENT
    assert retrieved[1].state == NotificationState.REJECTED
    assert get_latest_email() is None


def test_throttling_sql_rate_limiter_different_types(
    email_server, session, create_notification
):
    session.execute(
        text(
            "INSERT INTO notification_configs (notification_type, days, hours, minutes, quota)"
            f" VALUES ('{NotificationType.NEWS.value}', 0, 0, 1, 1)"
        )
    )

    session.execute(
        text(
            "INSERT INTO notifications (from_email, to_email, subject, body, notification_type, state, last_updated)"
            f" VALUES ('from-1234@email.com', 'to-1234@email.com', 'Example Subject', 'Example body content', "
            f" '{NotificationType.NEWS.value}', '{NotificationState.SENT.value}', CURRENT_TIMESTAMP)"
        )
    )
    email_sender = EmailSender(email_server)
    repo = NotificationRepository(session)
    rate_limiter = SqlRateLimiter(session, NotificationConfigRepository(session))
    notification = create_notification(NotificationType.NEWS)
    service.send_notification(notification, email_sender, repo, rate_limiter)
    notification = create_notification(NotificationType.STATUS)
    service.send_notification(notification, email_sender, repo, rate_limiter)
    notification = create_notification(NotificationType.MARKETING)
    service.send_notification(notification, email_sender, repo, rate_limiter)
    retrieved = repo.list()
    assert len(retrieved) == 4
    assert retrieved[0].state == NotificationState.SENT  # this is not a real sent email
    assert retrieved[1].state == NotificationState.REJECTED
    assert retrieved[2].state == NotificationState.SENT
    assert retrieved[3].state == NotificationState.SENT
    assert count_emails() == 2


def test_create_notification_config_saves_config(session):
    repo = NotificationConfigRepository(session)
    service.create_notification_config(NotificationType.NEWS, 1, 2, 30, 100, repo)

    config = repo.find_by_type(NotificationType.NEWS)
    assert config is not None
    assert config.days == 1
    assert config.hours == 2
    assert config.minutes == 30
    assert config.quota == 100


def test_create_notification_config_correct_attributes(session):
    repo = NotificationConfigRepository(session)
    service.create_notification_config(NotificationType.MARKETING, 0, 5, 0, 50, repo)

    config = repo.find_by_type(NotificationType.MARKETING)
    assert config.notification_type == NotificationType.MARKETING
    assert config.days == 0
    assert config.hours == 5
    assert config.minutes == 0
    assert config.quota == 50
