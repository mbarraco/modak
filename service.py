from adapters import AbstractEmailSender, AbstractRateLimiter, NotificationRepository
from model import Notification


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
