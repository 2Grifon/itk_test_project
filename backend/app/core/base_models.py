from datetime import datetime, timezone
import uuid

from sqlmodel import Field, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


class UUIDModelBase(SQLModel):
    """Базовый класс для моделей с UUID в качестве первичного ключа."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
