from adapters import (
    AbstractEmailSender,
    AbstractRateLimiter,
    NotificationRepository,
    NotificationConfigRepository,
)
from domain.model import Notification, NotificationConfig, NotificationType


def send_notification(
    notification: Notification,
    email_sender: AbstractEmailSender,
    repo: NotificationRepository,
    rate_limiter: AbstractRateLimiter,
):
    if rate_limiter.shall_pass(notification):
        errors = email_sender.send_email(notification)
        _ = errors  #  explicitelly ignoring errors for this version
        notification.mark_sent()
    else:
        notification.mark_rejected()
    notification.mark_updated()
    repo.add(notification)
    repo.session.commit()


def create_notification_config(
    notification_type: NotificationType,
    days: int,
    hours: int,
    minutes: int,
    quota: int,
    repo: NotificationConfigRepository,
):
    """TODO: make this atomic to be able to rollback"""
    existing_config = repo.find_by_type(notification_type)
    if existing_config:
        repo.session.delete(existing_config)
    repo.session.commit()

    notification_config = NotificationConfig(
        notification_type=notification_type,
        days=days,
        hours=hours,
        minutes=minutes,
        quota=quota,
    )

    repo.add(notification_config)
    repo.session.commit()


def get_all_notification_configs(repo: NotificationConfigRepository):
    """
    Retrieves all notification configurations from the database.

    :param repo: The repository to retrieve the notification configurations.
    :return: A list of all NotificationConfig instances.
    """
    return repo.list()
