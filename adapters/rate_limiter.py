import abc
from datetime import datetime, timedelta
from typing import Optional

from redis import Redis
from sqlalchemy.orm import Session

from domain.model import Notification

from . import NotificationConfigRepository


class AbstractRateLimiter(abc.ABC):
    @abc.abstractclassmethod
    def shall_pass(notification: Notification) -> bool:
        raise NotImplementedError


class SqlRateLimiter(AbstractRateLimiter):
    def __init__(self, session: Session, repo: NotificationConfigRepository):
        self.session = session
        self.repo = repo

    def shall_pass(self, notification: Notification) -> bool:
        config = self.repo.find_by_type(notification.notification_type)
        if not config:
            return True

        time_limit = datetime.utcnow() - timedelta(
            days=config.days, hours=config.hours, minutes=config.minutes
        )
        recent_notifications_count = (
            self.session.query(Notification)
            .filter(
                Notification.notification_type == notification.notification_type,
                Notification.last_updated > time_limit,
            )
            .count()
        )

        return recent_notifications_count < config.quota


from datetime import datetime, timedelta
from domain.model import Notification

from datetime import datetime
from domain.model import Notification


class RedisRateLimiter:
    def __init__(self, redis_client: Redis, repo: NotificationConfigRepository):
        self.redis_client = redis_client
        self.repo = repo

    def _bucket_key(self, notification: Notification) -> str:
        return f"rate_limiter:{notification.to_email}:{notification.notification_type}"

    def shall_pass(self, notification: Notification) -> bool:
        config = self.repo.find_by_type(notification.notification_type)
        bucket_key = self._bucket_key(notification)
        token_count, last_reset = self._get_bucket(bucket_key)
        if token_count is None:
            token_count = config.quota
            last_reset = int(datetime.now().timestamp())

        now = datetime.now().timestamp()

        # Reset the token count if the reset interval has passed
        if now - last_reset > config.interval_in_seconds:
            token_count = config.quota
            last_reset = now

        if token_count > 0:
            # Consume a token
            self._update_bucket(bucket_key, token_count - 1, last_reset)
            return True
        else:
            return False

    def _get_bucket(self, key: str) -> Optional[tuple]:
        data = self.redis_client.get(key)
        token_count, last_reset = None, None
        if data:
            token_count, last_reset = map(int, data.decode().split(","))
        return token_count, last_reset

    def _update_bucket(self, key: str, token_count: int, last_reset: int) -> None:
        data = f"{token_count},{last_reset}"
        self.redis_client.set(key, data)
