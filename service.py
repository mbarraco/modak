from adapters import AbstractEmailSender, NotificationRepository
from model import Notification


def send_notification(notification: Notification, email_sender: AbstractEmailSender, repo: NotificationRepository):
    errors = email_sender.send_email(notification)
    _ =  errors  #  explicitelly ignoring errors for this version
    notification.mark_sent()
    notification.mark_updated()
    repo.add(notification)
    repo.session.commit()




