from datetime import datetime

from sqlalchemy import CHAR, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fems_fastApi.db.base import Base


class User(Base):
    """User model for authentication."""

    __tablename__ = "TB_BASE_USER"

    user_id: Mapped[str] = mapped_column("USER_ID", String(50), primary_key=True)
    mill_cd: Mapped[str | None] = mapped_column("MILL_CD", String(50), nullable=True)
    plant_code: Mapped[str | None] = mapped_column("PLANT_CODE", String(50), nullable=True)
    user_nm: Mapped[str | None] = mapped_column("USER_NM", String(100), nullable=True)
    password: Mapped[str] = mapped_column("USER_PW", String(255), nullable=False)
    tel: Mapped[str | None] = mapped_column("TEL", String(100), nullable=True)
    login_dt: Mapped[datetime | None] = mapped_column("LOGIN_DT", DateTime, nullable=True)
    logout_dt: Mapped[datetime | None] = mapped_column("LOGOUT_DT", DateTime, nullable=True)
    login_status: Mapped[str | None] = mapped_column("LOGIN_STATUS", String(10), nullable=True)
    ip_addr: Mapped[str | None] = mapped_column("IP_ADDR", String(50), nullable=True)
    use_dt: Mapped[str | None] = mapped_column("USE_DT", String(8), nullable=True)
    use_yn: Mapped[str | None] = mapped_column("USE_YN", CHAR(1), default="Y")
    admin_yn: Mapped[str | None] = mapped_column("ADMIN_YN", CHAR(1), nullable=True)
    cre_user: Mapped[str | None] = mapped_column("CRE_USER", String(50), nullable=True)
    cre_dt: Mapped[datetime | None] = mapped_column("CRE_DT", DateTime, server_default=func.now())
    upd_user: Mapped[str | None] = mapped_column("UPD_USER", String(50), nullable=True)
    upd_dt: Mapped[datetime | None] = mapped_column("UPD_DT", DateTime, nullable=True)
