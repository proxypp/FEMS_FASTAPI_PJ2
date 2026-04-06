from datetime import datetime

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fems_fastApi.db.base import Base


class Equip(Base):
    """Equipment model for TB_BASE_EQUIP."""

    __tablename__ = "TB_BASE_EQUIP"
    __table_args__ = {"schema": "dbo"}

    mill_cd: Mapped[str | None] = mapped_column("MILL_CD", String(50), nullable=True)
    plant_code: Mapped[str | None] = mapped_column("PLANT_CODE", String(50), nullable=True)
    equip_code: Mapped[str] = mapped_column("EQUIP_CODE", String(50), primary_key=True)
    rout_code: Mapped[str | None] = mapped_column("ROUT_CODE", String(50), nullable=True)
    equip_name: Mapped[str | None] = mapped_column("EQUIP_NAME", String(200), nullable=True)
    equip_gbn: Mapped[str | None] = mapped_column("EQUIP_GBN", String(50), nullable=True)
    equip_type: Mapped[str | None] = mapped_column("EQUIP_TYPE", String(50), nullable=True)
    equip_spec: Mapped[str | None] = mapped_column("EQUIP_SPEC", String(500), nullable=True)
    buy_dt: Mapped[str | None] = mapped_column("BUY_DT", String(8), nullable=True)
    disuse_dt: Mapped[str | None] = mapped_column("DISUSE_DT", String(8), nullable=True)
    equip_model: Mapped[str | None] = mapped_column("EQUIP_MODEL", String(200), nullable=True)
    equip_cost: Mapped[float | None] = mapped_column("EQUIP_COST", Numeric(18, 4), nullable=True)
    equip_no: Mapped[str | None] = mapped_column("EQUIP_NO", String(100), nullable=True)
    equip_tp: Mapped[str | None] = mapped_column("EQUIP_TP", String(50), nullable=True)
    equip_capa: Mapped[str | None] = mapped_column("EQUIP_CAPA", String(200), nullable=True)
    equip_j: Mapped[str | None] = mapped_column("EQUIP_J", String(200), nullable=True)
    equip_cust: Mapped[str | None] = mapped_column("EQUIP_CUST", String(200), nullable=True)
    remark: Mapped[str | None] = mapped_column("REMARK", String(500), nullable=True)
    cre_user: Mapped[str | None] = mapped_column("CRE_USER", String(50), nullable=True)
    cre_dt: Mapped[datetime | None] = mapped_column("CRE_DT", DateTime, server_default=func.now())
    upd_user: Mapped[str | None] = mapped_column("UPD_USER", String(50), nullable=True)
    upd_dt: Mapped[datetime | None] = mapped_column("UPD_DT", DateTime, nullable=True)
