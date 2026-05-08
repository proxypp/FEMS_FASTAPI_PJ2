from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator


class EnergyAmountTrendResponse(BaseModel):
    utility_date: str | None = None
    unit: str | None = None
    energy_type: str | None = None
    utility_amount: float | None = None

    model_config = {"from_attributes": True}

    @field_validator("utility_date", mode="before")
    @classmethod
    def coerce_date(cls, v: object) -> str | None:
        if v is None:
            return None
        if isinstance(v, (datetime, date)):
            return v.strftime("%Y-%m-%d")
        return str(v)

    @field_validator("utility_amount", mode="before")
    @classmethod
    def coerce_amount(cls, v: object) -> float | None:
        if v is None:
            return None
        if isinstance(v, Decimal):
            return float(v)
        return v
