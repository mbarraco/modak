import abc
from datetime import datetime, timedelta
from typing import Optional

from redis import Redis
from sqlalchemy.orm import Session

from domain.model import Notification, NotificationConfig, NotificationState

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

        time_limit = datetime.utcnow() - timedelta(seconds=config.interval_in_seconds)
        recent_notifications_count = (
            self.session.query(Notification)
            .filter(
                Notification.notification_type == notification.notification_type,
                Notification.state == NotificationState.SENT,
                Notification.last_updated > time_limit,
                Notification.to_email == notification.to_email,
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
        if config is None:
            return True
        bucket_key = self._bucket_key(notification)
        token_count, last_reset = self._get_or_initialize_bucket_values(
            bucket_key, config
        )

        now = datetime.now().timestamp()

        if self._should_reset_tokens(now, last_reset, config.interval_in_seconds):
            token_count, last_reset = config.quota, now
        if token_count > 0:
            self._update_bucket(bucket_key, token_count - 1, last_reset)
            return True
        else:
            return False

    def _get_or_initialize_bucket_values(
        self, key: str, config: NotificationConfig
    ) -> tuple[int, int]:
        data = self.redis_client.get(key)
        if data:
            token_count, last_reset = map(float, data.decode().split(","))
        else:
            token_count = config.quota
            last_reset = float(datetime.now().timestamp())
        return token_count, last_reset

    def _should_reset_tokens(
        self, now: int, last_reset: int, interval_seconds: int
    ) -> bool:
        return now - last_reset > interval_seconds

    def _update_bucket(self, key: str, token_count: int, last_reset: int) -> None:
        data = f"{token_count},{last_reset}"
        self.redis_client.set(key, data)
