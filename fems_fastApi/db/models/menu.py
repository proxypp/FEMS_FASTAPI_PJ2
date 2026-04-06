from datetime import datetime

from sqlalchemy import CHAR, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fems_fastApi.db.base import Base


class ConfMenu(Base):
    """메뉴 설정 모델 (TB_CONF_MENU)."""

    __tablename__ = "TB_CONF_MENU"

    menu_id: Mapped[str] = mapped_column("MENU_ID", String(50), primary_key=True)
    menu_name: Mapped[str | None] = mapped_column("MENU_NAME", String(100), nullable=True)
    parent_id: Mapped[str | None] = mapped_column("PARENT_ID", String(50), nullable=True)
    menu_type: Mapped[str | None] = mapped_column("MENU_TYPE", CHAR(1), nullable=True)
    use_yn: Mapped[str | None] = mapped_column("USE_YN", CHAR(1), nullable=True)
    dis_sort: Mapped[int | None] = mapped_column("DISSORT", nullable=True)


class ConfUserMenu(Base):
    """사용자 메뉴 권한 모델 (TB_CONF_USER)."""

    __tablename__ = "TB_CONF_USER"

    mill_cd: Mapped[str | None] = mapped_column("MILL_CD", String(50), nullable=True)
    user_id: Mapped[str] = mapped_column("USER_ID", String(50), primary_key=True)
    parent_id: Mapped[str | None] = mapped_column("PARENT_ID", String(50), nullable=True)
    menu_id: Mapped[str] = mapped_column("MENU_ID", String(50), primary_key=True)
    use_yn: Mapped[str | None] = mapped_column("USE_YN", CHAR(1), nullable=True)
    cre_user: Mapped[str | None] = mapped_column("CRE_USER", String(50), nullable=True)
    cre_dt: Mapped[datetime | None] = mapped_column("CRE_DT", DateTime, server_default=func.now())
    upd_user: Mapped[str | None] = mapped_column("UPD_USER", String(50), nullable=True)
    upd_dt: Mapped[datetime | None] = mapped_column("UPD_DT", DateTime, nullable=True)
