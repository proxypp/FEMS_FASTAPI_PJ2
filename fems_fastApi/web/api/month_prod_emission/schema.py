from decimal import Decimal

from pydantic import BaseModel, Field


class MonthProdEmissionResponse(BaseModel):
    """월 생산량/배출 조회 결과 (USP_MONTH_PROD_EMISSION_SEARCH - GRID_GBN='M')."""

    year: str | None = None
    month_01: Decimal | None = Field(None, validation_alias="01월")
    month_02: Decimal | None = Field(None, validation_alias="02월")
    month_03: Decimal | None = Field(None, validation_alias="03월")
    month_04: Decimal | None = Field(None, validation_alias="04월")
    month_05: Decimal | None = Field(None, validation_alias="05월")
    month_06: Decimal | None = Field(None, validation_alias="06월")
    month_07: Decimal | None = Field(None, validation_alias="07월")
    month_08: Decimal | None = Field(None, validation_alias="08월")
    month_09: Decimal | None = Field(None, validation_alias="09월")
    month_10: Decimal | None = Field(None, validation_alias="10월")
    month_11: Decimal | None = Field(None, validation_alias="11월")
    month_12: Decimal | None = Field(None, validation_alias="12월")

    model_config = {"populate_by_name": True}
