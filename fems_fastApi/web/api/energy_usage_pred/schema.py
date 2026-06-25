from pydantic import BaseModel, Field, field_validator


class EnergyUsagePredResponse(BaseModel):
    """에너지 사용예측 조회 결과 (USP_ENERGY_USAGE_PRED_SEARCH - GRID_GBN='M', DML_GBN='S')."""

    utility_date: str | None = Field(None, alias="UTILITY_DATE")

    @field_validator("utility_date", mode="before")
    @classmethod
    def coerce_date_to_str(cls, v: object) -> str | None:
        if v is None:
            return None
        return str(v) if not isinstance(v, str) else v
    source_id: str | None = Field(None, alias="SOURCE_ID")
    source_name: str | None = Field(None, alias="SOURCE_NAME")
    utility_used: float | None = Field(None, alias="UTILITY_USED")
    pred_used: float | None = Field(None, alias="PRED_USED")
    unit: str | None = Field(None, alias="UNIT")
    erroramt: float | None = Field(None, alias="ERRORAMT")
    errorrate: float | None = Field(None, alias="ERRORRATE")
    accuracy: float | None = Field(None, alias="ACCURACY")

    model_config = {"from_attributes": True, "populate_by_name": True}
