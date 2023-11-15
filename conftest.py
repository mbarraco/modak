import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from config import EMAIL_SERVER_HOST, EMAIL_SERVER_PORT, EMAIL_SERVER_WEB_PORT
from email_server import EmailServer
from model import Notification, NotificationType
from orm import metadata, start_mappers


@pytest.fixture
def notification_news():
    def _create_notification() -> Notification:
        return Notification(
            f"from-{uuid4()}@modak.com",
            "this is the body",
            "fresh news",
            f"to-{uuid4()}@modak.com",
            NotificationType.NEWS,
        )
    return _create_notification

@pytest.fixture
def email_server():
    server = EmailServer(EMAIL_SERVER_HOST, EMAIL_SERVER_PORT)
    yield server
    server.close()


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
