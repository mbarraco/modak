import requests
from config import EMAIL_SERVER_HOST, EMAIL_SERVER_WEB_PORT


def clear_all_emails():
    try:
        response = requests.delete(
            f"http://{EMAIL_SERVER_HOST}:{EMAIL_SERVER_WEB_PORT}/api/v1/messages"
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


def get_email_data():
    try:
        response = requests.get(
            f"http://{EMAIL_SERVER_HOST}:{EMAIL_SERVER_WEB_PORT}/api/v2/messages"
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_latest_email():
    """TODO: can be optimized by asking for only 1 email"""
    data = get_email_data()
    if data and data["items"]:
        return data["items"][0]
    return None


def count_emails():
    data = get_email_data()
    if data:
        return len(data["items"])
    return 0
