from sqlalchemy import text

import service
from adapters import (
    EmailSender,
    NotificationRepository,
    NotificationConfigRepository,
    SqlRateLimiter,
)
from model import Notification, NotificationState, NotificationType
from test_utils import count_emails, get_latest_email


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
