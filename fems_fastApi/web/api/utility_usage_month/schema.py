from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class UtilityUsageMonthRequest(BaseModel):
    """Utility usage month request schema."""

    mill_cd: str | None = None
    utility_type: str | None = None
    supplier_contract_no: str | None = None
    contract_type: str | None = None
    contract_power_kw: Decimal | None = None
    bill_cycle_type: str | None = None
    bill_ym: str | None = None
    bill_dt: str | None = None
    usage_start_dt: datetime | None = None
    usage_end_dt: datetime | None = None
    metering_days: int | None = None
    bill_no: str | None = None
    prev_reading_kwh: Decimal | None = None
    curr_reading_kwh: Decimal | None = None
    usage_kwh: Decimal | None = None
    peak_usage_kwh: Decimal | None = None
    mid_usage_kwh: Decimal | None = None
    off_usage_kwh: Decimal | None = None
    max_demand_kw: Decimal | None = None
    power_factor_pct: Decimal | None = None
    attach_file_url: str | None = None
    remark: str | None = None
    status: str | None = None
    cre_user: str | None = None
    cre_dt: datetime | None = None
    upd_user: str | None = None
    upd_dt: datetime | None = None


class UtilityUsageMonthResponse(BaseModel):
    """Utility usage month response schema."""

    utility_usage_id: int
    mill_cd: str | None = None
    utility_type: str | None = None
    supplier_contract_no: str | None = None
    contract_type: str | None = None
    contract_power_kw: Decimal | None = None
    bill_cycle_type: str | None = None
    bill_ym: str | None = None
    bill_dt: str | None = None
    usage_start_dt: datetime | None = None
    usage_end_dt: datetime | None = None
    metering_days: int | None = None
    bill_no: str | None = None
    prev_reading_kwh: Decimal | None = None
    curr_reading_kwh: Decimal | None = None
    usage_kwh: Decimal | None = None
    peak_usage_kwh: Decimal | None = None
    mid_usage_kwh: Decimal | None = None
    off_usage_kwh: Decimal | None = None
    max_demand_kw: Decimal | None = None
    power_factor_pct: Decimal | None = None
    attach_file_url: str | None = None
    remark: str | None = None
    status: str | None = None
    cre_user: str | None = None
    cre_dt: datetime | None = None
    upd_user: str | None = None
    upd_dt: datetime | None = None

    model_config = {"from_attributes": True}
