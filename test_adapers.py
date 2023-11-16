from adapters import EmailSender
from model import Notification, NotificationType
from test_utils import get_latest_email


def test_message_is_correctly_sent(email_server):
    email_sender = EmailSender(email_server)

    email_content = Notification(
        "sender@monak.com",
        "this is a test message!",
        "test message 01",
        "receiver@monak.com",
        NotificationType.MARKETING,
    )
    email_sender.send_email(email_content)
    latest_email = get_latest_email()
    assert "sender@monak.com" == latest_email["Raw"]["From"]
    assert ["receiver@monak.com"] == latest_email["Raw"]["To"]
    assert "this is a test message!" == latest_email["Content"]["Body"]
    assert ["test message 01"] == latest_email["Content"]["Headers"]["Subject"]
