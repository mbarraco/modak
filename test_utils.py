import requests
from config import EMAIL_SERVER_HOST, EMAIL_SERVER_WEB_PORT


def get_latest_email():
    response = requests.get(
        f"http://{EMAIL_SERVER_HOST}:{EMAIL_SERVER_WEB_PORT}/api/v2/messages"
    )
    response.raise_for_status()
    data = response.json()
    return data["items"][0] if data["items"] else None
