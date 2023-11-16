from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    Enum,
    String,
    DateTime,
    CheckConstraint,
)
from sqlalchemy.orm import registry

from domain.model import (
    NotificationConfig,
    Notification,
    NotificationState,
    NotificationType,
)

mapper_registry = registry()


metadata = MetaData()

notification_configs = Table(
    "notification_configs",
    metadata,
    Column("id", Integer, primary_key=True),  # Primary key column
    Column("notification_type", Enum(NotificationType), nullable=False, unique=True),
    Column("seconds", Integer, nullable=False),
    Column("quota", Integer, nullable=False),
    CheckConstraint("quota >= 1", name="check_quota_min"),
)

notifications = Table(
    "notifications",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("from_email", String(255), nullable=False),
    Column("to_email", String(255), nullable=False),
    Column("subject", String(255), nullable=False),
    Column("body", String, nullable=False),
    Column("notification_type", Enum(NotificationType), nullable=False),
    Column("state", Enum(NotificationState), nullable=False),
    Column("last_updated", DateTime, nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(Notification, notifications)
    mapper_registry.map_imperatively(NotificationConfig, notification_configs)
