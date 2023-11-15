from copy import deepcopy

from adapters import EmailSender, NotificationRepository
from model import Notification, NotificationType
from service import send_notification
from test_utils import get_latest_email


def test_send_notification(email_server, session, notification_news):
    email_sender = EmailSender(email_server)
    repo = NotificationRepository(session)
    notification: Notification = notification_news()
    send_notification(notification, email_sender, repo)

    latest_email = get_latest_email()
    assert notification.from_email == latest_email["Raw"]["From"]
    assert [notification.to_email]  == latest_email["Raw"]["To"]
    assert notification.body == latest_email["Content"]["Body"]
    assert [notification.subject] == latest_email["Content"]["Headers"]["Subject"]


def test_do_send_email_saves_notification(email_server, session, notification_news):
    email_sender = EmailSender(email_server)
    repo = NotificationRepository(session)
    notification = notification_news()
    send_notification(notification, email_sender, repo)

    retrieved = repo.list()
    assert len(retrieved) == 1
    retrieved[0] == notification

