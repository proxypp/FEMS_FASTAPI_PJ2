from sqlalchemy.orm import DeclarativeBase

from fems_fastApi.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
