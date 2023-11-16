import questionary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Notification, NotificationType
from service import send_notification
from email_server import EmailServer
from config import EMAIL_SERVER_HOST, EMAIL_SERVER_PORT


from adapters import (
    EmailSender,
    NotificationRepository,
    NotificationConfigRepository,
    SqlRateLimiter,
)
from model import Notification, NotificationType

from orm import metadata, start_mappers
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///:memory:")
metadata.create_all(engine)
start_mappers()
session = sessionmaker(bind=engine)()


def main():
    to_email = questionary.text("Enter recipient email address:").ask()
    from_email = questionary.text("Enter recipient email address:").ask()
    subject = questionary.text("Enter email subject:").ask()
    body = questionary.text("Enter email body:").ask()
    notification_type = questionary.select(
        "Select notification type:", choices=[nt.value for nt in NotificationType]
    ).ask()

    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    email_server = EmailServer(EMAIL_SERVER_HOST, EMAIL_SERVER_PORT)
    email_sender = EmailSender(email_server)
    repo = NotificationRepository(session)
    rate_limiter = SqlRateLimiter(session, NotificationConfigRepository(session))

    # Create a notification object
    try:
        notification = Notification(
            from_email=from_email,  # Replace with actual sender email
            to_email=to_email,
            subject=subject,
            body=body,
            notification_type=NotificationType[notification_type],
        )

        # Send the notification
        send_notification(notification, email_sender, repo, rate_limiter)
    except ValueError as e:
        print(f"You provideda an invalid value:\n {e}")
    except Exception as e:
        print(f"Unexpected error:\n {e}")


if __name__ == "__main__":
    main()
