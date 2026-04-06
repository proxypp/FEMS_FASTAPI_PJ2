from datetime import datetime

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fems_fastApi.db.base import Base


class Item(Base):
    """Item model for TB_BASE_ITEM."""

    __tablename__ = "TB_BASE_ITEM"
    __table_args__ = {"schema": "dbo"}

    mill_cd: Mapped[str | None] = mapped_column("MILL_CD", String(50), nullable=True)
    item_code: Mapped[str] = mapped_column("ITEM_CODE", String(50), primary_key=True)
    item_name: Mapped[str | None] = mapped_column("ITEM_NAME", String(200), nullable=True)
    item_type: Mapped[str | None] = mapped_column("ITEM_TYPE", String(50), nullable=True)
    item_wet: Mapped[float | None] = mapped_column("ITEM_WET", Numeric(18, 4), nullable=True)
    start_dt: Mapped[str | None] = mapped_column("START_DT", String(8), nullable=True)
    end_dt: Mapped[str | None] = mapped_column("END_DT", String(8), nullable=True)
    grade: Mapped[str | None] = mapped_column("GRADE", String(50), nullable=True)
    color: Mapped[str | None] = mapped_column("COLOR", String(50), nullable=True)
    remark: Mapped[str | None] = mapped_column("REMARK", String(500), nullable=True)
    cre_user: Mapped[str | None] = mapped_column("CRE_USER", String(50), nullable=True)
    cre_dt: Mapped[datetime | None] = mapped_column("CRE_DT", DateTime, server_default=func.now())
    upd_user: Mapped[str | None] = mapped_column("UPD_USER", String(50), nullable=True)
    upd_dt: Mapped[datetime | None] = mapped_column("UPD_DT", DateTime, nullable=True)
