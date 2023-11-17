import questionary
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.model import Notification, NotificationType
from service.service import (
    send_notification,
    create_notification_config,
    get_all_notification_configs,
)
from adapters.email_server import EmailServer
from config import EMAIL_SERVER_HOST, EMAIL_SERVER_PORT, REDIS_HOST, REDIS_PORT

from adapters import (
    EmailSender,
    NotificationRepository,
    NotificationConfigRepository,
    SqlRateLimiter,
    RedisRateLimiter,
)
from domain.model import Notification, NotificationType
from adapters.orm import metadata, start_mappers

engine = create_engine("sqlite:///database.db")
metadata.create_all(engine)
start_mappers()
Session = sessionmaker(bind=engine)
session = Session()

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT)


def send_email_workflow(session, redis_client):
    to_email = questionary.text("Enter recipient email address:").ask()
    from_email = questionary.text("Enter sender email address:").ask()
    subject = questionary.text("Enter email subject:").ask()
    body = questionary.text("Enter email body:").ask()
    notification_type = questionary.select(
        "Select notification type:", choices=[nt.value for nt in NotificationType]
    ).ask()

    email_server = EmailServer(EMAIL_SERVER_HOST, EMAIL_SERVER_PORT)
    email_sender = EmailSender(email_server)
    repo = NotificationRepository(session)
    rate_limiter = SqlRateLimiter(session, NotificationConfigRepository(session))
    # rate_limiter = RedisRateLimiter(redis_client, NotificationConfigRepository(session))

    try:
        notification = Notification(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            body=body,
            notification_type=NotificationType[notification_type],
        )

        state = send_notification(notification, email_sender, repo, rate_limiter)
        print(f"Email has been {state}.")
    except ValueError as e:
        print(f"Invalid value provided:\n {e}")


def create_notification_config_workflow(session):
    notification_type = questionary.select(
        "Select notification type:", choices=[nt.value for nt in NotificationType]
    ).ask()
    seconds = questionary.text("Enter number of seconds for rate limit:").ask()
    quota = questionary.text("Enter quota for rate limit:").ask()

    repo = NotificationConfigRepository(session)

    try:
        create_notification_config(
            NotificationType[notification_type], int(seconds), int(quota), repo
        )
        print("Notification configuration created successfully.")
    except ValueError as e:
        print(f"Invalid value provided:\n {e}")
    except Exception as e:
        print(f"Unexpected error:\n {e}")


def show_all_notification_configs_workflow(session):
    repo = NotificationConfigRepository(session)
    configs = get_all_notification_configs(repo)

    if not configs:
        print("No notification configurations found.")
        return

    for config in configs:
        print(
            f"Type: {config.notification_type}, seconds: {config.seconds}, Quota: {config.quota}"
        )


def main():
    choice = questionary.select(
        "Choose an action:",
        choices=[
            "Send Email",
            "Create Notification Config",
            "Show All Notification Configs",
        ],
    ).ask()

    if choice == "Send Email":
        send_email_workflow(session, redis_client)
    elif choice == "Create Notification Config":
        create_notification_config_workflow(session)
    elif choice == "Show All Notification Configs":
        show_all_notification_configs_workflow(session)


if __name__ == "__main__":
    main()
