from model import Notification, NotificationConfig, NotificationType

from sqlalchemy import text


def test_load_notification_config(session):
    session.execute(
        text(
            "INSERT INTO notification_configs (notification_type, days, hours, minutes, quota) VALUES "
            '("MARKETING", 1, 0, 0, 10),'
            '("STATUS", 0, 1, 0, 100),'
            '("NEWS", 0, 0, 1, 1000)'
        )
    )
    expected = [
        NotificationConfig("MARKETING", 1, 0, 0, 10),
        NotificationConfig("STATUS", 0, 1, 0, 100),
        NotificationConfig("NEWS", 0, 0, 1, 1000),
    ]
    retrieved: list[NotificationConfig] = session.query(NotificationConfig).all()
    assert len(retrieved) == 3
    retrieved[0].notification_type == "MARKETING"
    retrieved[0].days == 1
    retrieved[0].hours == 0
    retrieved[0].minutes == 0

    retrieved[1].notification_type == "STATUS"
    retrieved[1].days == 0
    retrieved[1].hours == 1
    retrieved[1].minutes == 0

    retrieved[2].notification_type == "NEWS"
    retrieved[2].days == 0
    retrieved[2].hours == 0
    retrieved[2].minutes == 1


def test_notification_mapper_can_save(session):
    new_notification = Notification(
        "from@modak.com",
        "this is the body",
        "this is the subject",
        "to@modak.com",
        NotificationType.NEWS,
    )
    session.add(new_notification)
    session.commit()

    rows = list(
        session.execute(
            text(
                'SELECT from_email, body, subject, to_email, notification_type FROM "notifications"'
            )
        )
    )
    assert rows == [
        (
            "from@modak.com",
            "this is the body",
            "this is the subject",
            "to@modak.com",
            "NEWS",
        )
    ]


def test_notification_mapper_can_load(session):
    new_notification = Notification(
        "from@modak.com",
        "this is the body",
        "this is the subject",
        "to@modak.com",
        NotificationType.NEWS,
    )
    session.add(new_notification)
    session.commit()
    assert session.query(Notification).one() == new_notification
