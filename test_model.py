import pytest
from model import EmailContent, Notification, NotificationType


def test_valid_notification():
    content = EmailContent(
        "from@modak.com",
        "this is the body",
        "this is the subject",
        "to@modak.com",
    )
    Notification(content, NotificationType.DAILY_NEWS)

def test_invalid_notification_from_address():
    content = EmailContent(
        ".com",
        "this is the body",
        "this is the subject",
        "to@modak.com",
    )

    with pytest.raises(ValueError):
        Notification(content, NotificationType.DAILY_NEWS)


def test_invalid_notification_to_address():
    content = EmailContent(
        "from@modak.com",
        "this is the body",
        "this is the subject",
        "to@modak",
    )
    with pytest.raises(ValueError):
        Notification(content, NotificationType.DAILY_NEWS)