import pytest
from model import Notification, Notification, NotificationType


def test_invalid_notification_from_address():
    with pytest.raises(ValueError):
        Notification(
            ".com",
            "this is the body",
            "this is the subject",
            "to@modak.com",
            NotificationType.NEWS,
        )


def test_invalid_notification_to_address():
    with pytest.raises(ValueError):
        Notification(
            "from@modak.com",
            "this is the body",
            "this is the subject",
            "to@modak",
            NotificationType.NEWS,
        )
