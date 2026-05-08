from datetime import date, datetime

from pydantic import BaseModel


class EquipInterfaceResponse(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    equip_code: str | None = None
    equip_name: str | None = None
    source_id: str | None = None
    source_name: str | None = None
    utility_date: date | None = None
    unit: str | None = None
    upd_dt: datetime | None = None
    utility_used: float | None = None

    model_config = {"from_attributes": True}
