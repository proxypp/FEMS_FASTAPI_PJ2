from datetime import datetime

from pydantic import BaseModel


class EquipCreateRequest(BaseModel):
    """Equipment create request schema."""

    mill_cd: str | None = None
    plant_code: str | None = None
    equip_code: str
    rout_code: str | None = None
    equip_name: str | None = None
    equip_gbn: str | None = None
    equip_type: str | None = None
    equip_spec: str | None = None
    buy_dt: str | None = None
    disuse_dt: str | None = None
    equip_model: str | None = None
    equip_cost: float | None = None
    equip_no: str | None = None
    equip_tp: str | None = None
    equip_capa: str | None = None
    equip_j: str | None = None
    equip_cust: str | None = None
    remark: str | None = None
    cre_user: str


class EquipUpdateRequest(BaseModel):
    """Equipment update request schema."""

    mill_cd: str | None = None
    plant_code: str | None = None
    rout_code: str | None = None
    equip_name: str | None = None
    equip_gbn: str | None = None
    equip_type: str | None = None
    equip_spec: str | None = None
    buy_dt: str | None = None
    disuse_dt: str | None = None
    equip_model: str | None = None
    equip_cost: float | None = None
    equip_no: str | None = None
    equip_tp: str | None = None
    equip_capa: str | None = None
    equip_j: str | None = None
    equip_cust: str | None = None
    remark: str | None = None
    upd_user: str | None = None


class EquipResponse(BaseModel):
    """Equipment response schema."""

    mill_cd: str | None = None
    plant_code: str | None = None
    equip_code: str
    rout_code: str | None = None
    equip_name: str | None = None
    equip_gbn: str | None = None
    equip_type: str | None = None
    equip_spec: str | None = None
    buy_dt: str | None = None
    disuse_dt: str | None = None
    equip_model: str | None = None
    equip_cost: float | None = None
    equip_no: str | None = None
    equip_tp: str | None = None
    equip_capa: str | None = None
    equip_j: str | None = None
    equip_cust: str | None = None
    remark: str | None = None
    cre_user: str | None = None
    cre_dt: datetime | None = None
    upd_user: str | None = None
    upd_dt: datetime | None = None

    model_config = {"from_attributes": True}


class EquipMeterCreateRequest(BaseModel):
    meter_id: str
    cre_user: str | None = None


class EquipMeterUpdateRequest(BaseModel):
    meter_id: str
    upd_user: str | None = None


class EquipMeterResponse(BaseModel):
    equip_code: str | None = None
    equip_name: str | None = None
    meter_id: str | None = None
    meter_name: str | None = None

    model_config = {"from_attributes": True}
