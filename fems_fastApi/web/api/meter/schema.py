from datetime import datetime

from pydantic import BaseModel


class MeterCreateRequest(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    meter_id: str
    meter_name: str | None = None
    meter_type: str | None = None
    meter_ip: str | None = None
    address: str | None = None
    source_id: str | None = None
    use_yn: str = "Y"
    cre_user: str | None = None


class MeterUpdateRequest(BaseModel):
    plant_code: str | None = None
    meter_name: str | None = None
    meter_type: str | None = None
    meter_ip: str | None = None
    address: str | None = None
    source_id: str | None = None
    use_yn: str | None = None
    upd_user: str | None = None


class MeterSourceResponse(BaseModel):
    source_id: str | None = None
    source_name: str | None = None

    model_config = {"from_attributes": True}


class MeterResponse(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    plant_name: str | None = None
    meter_id: str
    meter_name: str | None = None
    meter_ip: str | None = None
    meter_type: str | None = None
    address: str | None = None
    use_yn: str | None = None

    model_config = {"from_attributes": True}
