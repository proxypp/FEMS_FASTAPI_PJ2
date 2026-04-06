from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TariffCreateRequest(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    tariff_id: str
    source_id: str | None = None
    apply_date: datetime | None = None
    tariff_name: str | None = None
    base_price: Decimal | None = None
    unit_price: Decimal | None = None
    etc_price1: Decimal | None = None
    etc_price2: Decimal | None = None
    etc_price3: Decimal | None = None
    etc_price4: Decimal | None = None
    etc_price5: Decimal | None = None
    tex_per: Decimal | None = None
    add_price1: Decimal | None = None
    add_price2: Decimal | None = None
    add_price3: Decimal | None = None
    add_price4: Decimal | None = None
    add_price5: Decimal | None = None
    use_yn: str = "Y"
    cre_user: str | None = None


class TariffUpdateRequest(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    source_id: str | None = None
    apply_date: datetime | None = None
    tariff_name: str | None = None
    base_price: Decimal | None = None
    unit_price: Decimal | None = None
    etc_price1: Decimal | None = None
    etc_price2: Decimal | None = None
    etc_price3: Decimal | None = None
    etc_price4: Decimal | None = None
    etc_price5: Decimal | None = None
    tex_per: Decimal | None = None
    add_price1: Decimal | None = None
    add_price2: Decimal | None = None
    add_price3: Decimal | None = None
    add_price4: Decimal | None = None
    add_price5: Decimal | None = None
    use_yn: str | None = None
    upd_user: str | None = None


class TariffResponse(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    tariff_id: str
    source_id: str | None = None
    apply_date: datetime | None = None
    tariff_name: str | None = None
    base_price: Decimal | None = None
    unit_price: Decimal | None = None
    etc_price1: Decimal | None = None
    etc_price2: Decimal | None = None
    etc_price3: Decimal | None = None
    etc_price4: Decimal | None = None
    etc_price5: Decimal | None = None
    tex_per: Decimal | None = None
    add_price1: Decimal | None = None
    add_price2: Decimal | None = None
    add_price3: Decimal | None = None
    add_price4: Decimal | None = None
    add_price5: Decimal | None = None
    use_yn: str | None = None

    model_config = {"from_attributes": True}


class TariffSourceResponse(BaseModel):
    source_id: str
    source_name: str | None = None

    model_config = {"from_attributes": True}
