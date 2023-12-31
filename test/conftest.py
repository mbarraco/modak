import pytest
from redis import Redis
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from config import EMAIL_SERVER_HOST, EMAIL_SERVER_PORT, REDIS_HOST, REDIS_PORT
from adapters.email_server import EmailServer
from domain.model import Notification, NotificationType
from adapters.orm import metadata, start_mappers

from .test_utils import clear_all_emails


@pytest.fixture
def create_notification():
    def _create_notification(notification_type: NotificationType) -> Notification:
        return Notification(
            f"from-{uuid4()}@modak.com",
            "this is the body",
            "fresh news",
            f"to-{uuid4()}@modak.com",
            notification_type,
        )

    return _create_notification


@pytest.fixture
def email_server():
    server = EmailServer(EMAIL_SERVER_HOST, EMAIL_SERVER_PORT)
    yield server
    clear_all_emails()
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


@pytest.fixture(scope="session")
def redis_client():
    client = Redis(host=REDIS_HOST, port=REDIS_PORT)
    yield client
    client.flushdb()
