from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class EmissionFactorCreateRequest(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    factor_id: str
    source_id: str | None = None
    apply_date: datetime | None = None
    factor_name: str | None = None
    factor_val: Decimal | None = None
    cre_user: str | None = None


class EmissionFactorUpdateRequest(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    source_id: str | None = None
    apply_date: datetime | None = None
    factor_name: str | None = None
    factor_val: Decimal | None = None
    upd_user: str | None = None


class EmissionFactorResponse(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    factor_id: str
    source_id: str | None = None
    apply_date: datetime | None = None
    factor_name: str | None = None
    factor_val: Decimal | None = None

    model_config = {"from_attributes": True}


class EmissionFactorSourceResponse(BaseModel):
    source_id: str
    source_name: str | None = None

    model_config = {"from_attributes": True}
