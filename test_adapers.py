import requests

from adapters import EmailSender
from email_server import EmailServer
from model import EmailContent
from config import EMAIL_SERVER_HOST, EMAIL_SERVER_PORT, EMAIL_SERVER_WEB_PORT


def get_latest_email():
    response = requests.get(
        f"http://{EMAIL_SERVER_HOST}:{EMAIL_SERVER_WEB_PORT}/api/v2/messages"
    )
    response.raise_for_status()
    data = response.json()
    return data["items"][0] if data["items"] else None


def test_message_is_correctly_sent():
    server = EmailServer(EMAIL_SERVER_HOST, EMAIL_SERVER_PORT)
    email_sender = EmailSender(server)

    email_content = EmailContent(
        "sender@monak.com",
        "this is a test message!",
        "test message 01",
        "receiver@monak.com",
    )
    email_sender.send_email(email_content)
    latest_email = get_latest_email()
    assert "sender@monak.com" == latest_email["Raw"]["From"]
    assert ["receiver@monak.com"] == latest_email["Raw"]["To"]
    assert "this is a test message!" == latest_email["Content"]["Body"]
    assert ["test message 01"] == latest_email["Content"]["Headers"]["Subject"]
