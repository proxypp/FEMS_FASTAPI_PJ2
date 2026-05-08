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


# ── 설비점검코드 관리 (USP_EQUIP_DAILY_CODE_EDIT) ──────────────────────────

class EquipDailyCodeResponse(BaseModel):
    mill_cd: str | None = None
    rout_code: str | None = None
    equip_code: str | None = None
    equip_name: str | None = None
    equip_check: str | None = None
    magm_val: float | None = None
    magm_max: float | None = None
    magm_min: float | None = None
    std_max: float | None = None
    std_min: float | None = None
    rmax_val: float | None = None
    unit: str | None = None
    remark: str | None = None

    model_config = {"from_attributes": True}


class EquipDailyCodeSaveRequest(BaseModel):
    mill_cd: str = ""
    rout_code: str = ""
    equip_code: str = ""
    equip_check: str = ""
    magm_val: float = 0
    magm_max: float = 0
    magm_min: float = 0
    std_max: float = 0
    std_min: float = 0
    rmax_val: float = 0
    unit: str = ""
    remark: str = ""
    image_bin: str | None = None  # Base64 인코딩 문자열 (선택)
    cre_user: str = ""
    upd_user: str = ""


class EquipDailyCodeDeleteRequest(BaseModel):
    mill_cd: str
    rout_code: str
    equip_code: str
    equip_check: str


# ── 설비점검실적 관리 (USP_EQUIP_DAILY_CHECK_EDIT) ──────────────────────────

class EquipDailyCheckResponse(BaseModel):
    mill_cd: str | None = None
    rout_code: str | None = None
    equip_code: str | None = None
    equip_name: str | None = None
    equip_check: str | None = None
    check_yyyymm: str | None = None
    value_1: float | None = None
    value_2: float | None = None
    value_3: float | None = None
    value_4: float | None = None
    value_5: float | None = None
    value_6: float | None = None
    value_7: float | None = None
    value_8: float | None = None
    value_9: float | None = None
    value_10: float | None = None
    value_11: float | None = None
    value_12: float | None = None
    value_13: float | None = None
    value_14: float | None = None
    value_15: float | None = None
    value_16: float | None = None
    value_17: float | None = None
    value_18: float | None = None
    value_19: float | None = None
    value_20: float | None = None
    value_21: float | None = None
    value_22: float | None = None
    value_23: float | None = None
    value_24: float | None = None
    value_25: float | None = None
    value_26: float | None = None
    value_27: float | None = None
    value_28: float | None = None
    value_29: float | None = None
    value_30: float | None = None
    value_31: float | None = None

    model_config = {"from_attributes": True}


class EquipDailyCheckSaveRequest(BaseModel):
    mill_cd: str = ""
    rout_code: str = ""
    equip_code: str = ""
    equip_check: str = ""
    check_yyyymm: str = ""
    value_1: float = 0
    value_2: float = 0
    value_3: float = 0
    value_4: float = 0
    value_5: float = 0
    value_6: float = 0
    value_7: float = 0
    value_8: float = 0
    value_9: float = 0
    value_10: float = 0
    value_11: float = 0
    value_12: float = 0
    value_13: float = 0
    value_14: float = 0
    value_15: float = 0
    value_16: float = 0
    value_17: float = 0
    value_18: float = 0
    value_19: float = 0
    value_20: float = 0
    value_21: float = 0
    value_22: float = 0
    value_23: float = 0
    value_24: float = 0
    value_25: float = 0
    value_26: float = 0
    value_27: float = 0
    value_28: float = 0
    value_29: float = 0
    value_30: float = 0
    value_31: float = 0
    cre_user: str = ""
    upd_user: str = ""


class EquipDailyCheckDeleteRequest(BaseModel):
    mill_cd: str
    rout_code: str
    equip_code: str
    equip_check: str
    check_yyyymm: str
