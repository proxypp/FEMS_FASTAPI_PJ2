from decimal import Decimal

from pydantic import BaseModel, Field


class EquipCompareResponse(BaseModel):
    """설비간 비교분석 조회 결과 (GRID_GBN='M', DML_GBN='S')."""

    equip_code: str | None = Field(None, alias="EQUIP_CODE")
    equip_name: str | None = Field(None, alias="EQUIP_NAME")
    utility_amount: Decimal | None = Field(None, alias="UTILITY_AMOUNT")

    model_config = {"from_attributes": True, "populate_by_name": True}
