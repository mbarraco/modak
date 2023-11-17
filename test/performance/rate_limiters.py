import time
from datetime import datetime
from sqlalchemy import text


from domain.model import NotificationType
from adapters import (
    EmailSender,
    NotificationRepository,
    NotificationConfigRepository,
    RedisRateLimiter,
    SqlRateLimiter,
)
from service import service

import cProfile
import pstats

def performance_test_no_throttling(
    email_server, session, redis_client, create_notification
):
    email_sender = EmailSender(email_server)
    notification_repo = NotificationRepository(session)
    notification_config_repo = NotificationConfigRepository(session)
    sql_rate_limiter = SqlRateLimiter(session, notification_config_repo)
    redis_rate_limiter = RedisRateLimiter(redis_client, notification_config_repo)

    start_time = time.time()
    for _ in range(500):
        notification = create_notification(NotificationType.NEWS)
        service.send_notification(
            notification, email_sender, notification_repo, sql_rate_limiter
        )
    sql_duration = time.time() - start_time

    # Test with RedisRateLimiter
    start_time = time.time()
    for _ in range(500):
        notification = create_notification(NotificationType.NEWS)
        service.send_notification(
            notification, email_sender, notification_repo, redis_rate_limiter
        )
    redis_duration = time.time() - start_time

    print(f"SQL Rate Limiter Duration: {sql_duration} seconds")
    print(f"Redis Rate Limiter Duration: {redis_duration} seconds")


def performance_test_with_throttling(
    email_server, session, redis_client, create_notification, include_sql=True, include_redis=True
):
    session.execute(
        text(
            "INSERT INTO notification_configs (notification_type, seconds, quota)"
            f" VALUES ('{NotificationType.NEWS.value}', 60, 1)"
        )
    )

    email_sender = EmailSender(email_server)
    notification_repo = NotificationRepository(session)
    notification_config_repo = NotificationConfigRepository(session)
    sql_rate_limiter = SqlRateLimiter(session, notification_config_repo)
    redis_rate_limiter = RedisRateLimiter(redis_client, notification_config_repo)

    if include_sql:
        start_time = time.time()
        for _ in range(500):
            notification = create_notification(NotificationType.NEWS)
            notification.to_email = "to-sql@gmail.com"
            service.send_notification(
                notification, email_sender, notification_repo, sql_rate_limiter
            )
        print(f"{__name__}: SQL Rate Limiter Duration: { time.time() - start_time} seconds")


    if include_redis:
        start_time = time.time()
        for _ in range(500):
            notification = create_notification(NotificationType.NEWS)
            notification.to_email = "to-redis@gmail.com"
            service.send_notification(
                notification, email_sender, notification_repo, redis_rate_limiter
            )
        print(f"{__name__}: REDIS Rate Limiter Duration: { time.time() - start_time} seconds")



