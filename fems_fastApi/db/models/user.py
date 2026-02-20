from datetime import datetime

from sqlalchemy import CHAR, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fems_fastApi.db.base import Base


class User(Base):
    """User model for authentication."""

    __tablename__ = "user"

    user_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    user_nm: Mapped[str | None] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hp_no: Mapped[str | None] = mapped_column(String(100), nullable=True)
    remark: Mapped[str | None] = mapped_column(String(500), nullable=True)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    password_update_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    use_yn: Mapped[str | None] = mapped_column(CHAR(1), default="Y")
    del_yn: Mapped[str | None] = mapped_column(CHAR(1), default="N")
    admin_yn: Mapped[str | None] = mapped_column(CHAR(1), default="N")
    company: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cre_dt: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())
    cre_user: Mapped[str | None] = mapped_column(String(50), nullable=True)
    upd_dt: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    upd_user: Mapped[str | None] = mapped_column(String(50), nullable=True)