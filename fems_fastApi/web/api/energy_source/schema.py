from datetime import datetime

from pydantic import BaseModel


class EnergySourceCreateRequest(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    source_id: str
    source_name: str | None = None
    unit: str | None = None
    energy_type: str | None = None
    use_yn: str = "Y"
    cre_user: str | None = None


class EnergySourceUpdateRequest(BaseModel):
    plant_code: str | None = None
    source_name: str | None = None
    unit: str | None = None
    energy_type: str | None = None
    use_yn: str | None = None
    upd_user: str | None = None


class EnergySourceResponse(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    plant_name: str | None = None
    source_id: str
    source_name: str | None = None
    unit: str | None = None
    energy_type: str | None = None
    energy_type_name: str | None = None
    use_yn: str | None = None
    cre_user: str | None = None
    cre_dt: datetime | None = None
    upd_user: str | None = None
    upd_dt: datetime | None = None

    model_config = {"from_attributes": True}
