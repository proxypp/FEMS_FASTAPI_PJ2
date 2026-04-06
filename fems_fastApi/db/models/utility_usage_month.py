from datetime import datetime

from sqlalchemy import CHAR, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fems_fastApi.db.base import Base


class UtilityUsageMonth(Base):
    """Monthly utility usage model."""

    __tablename__ = "tb_utility_usage_month"
    __table_args__ = {"schema": "dbo"}

    utility_usage_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mill_cd: Mapped[str | None] = mapped_column("MILL_CD", String(50), nullable=True)
    utility_type: Mapped[str | None] = mapped_column("utility_type", String(50), nullable=True)
    supplier_contract_no: Mapped[str | None] = mapped_column(String(100), nullable=True)
    contract_type: Mapped[str | None] = mapped_column("contract_type", String(50), nullable=True)
    contract_power_kw: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    bill_cycle_type: Mapped[str | None] = mapped_column("bill_cycle_type", String(50), nullable=True)
    bill_ym: Mapped[str | None] = mapped_column(CHAR(6), nullable=True)
    bill_dt: Mapped[str | None] = mapped_column(String(8), nullable=True)
    usage_start_dt: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    usage_end_dt: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    metering_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bill_no: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prev_reading_kwh: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    curr_reading_kwh: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    usage_kwh: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    peak_usage_kwh: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    mid_usage_kwh: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    off_usage_kwh: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    max_demand_kw: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    power_factor_pct: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    attach_file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    remark: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str | None] = mapped_column("status", String(50), nullable=True)
    cre_user: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cre_dt: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())
    upd_user: Mapped[str | None] = mapped_column(String(50), nullable=True)
    upd_dt: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
