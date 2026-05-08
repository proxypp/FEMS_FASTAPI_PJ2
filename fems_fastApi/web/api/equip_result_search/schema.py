from pydantic import BaseModel, Field


class EquipResultSearchResponse(BaseModel):
    """설비가동조회 결과 (USP_EQUIP_RESULT_SEARCH - GRID_GBN='M', DML_GBN='S')."""

    equip_code: str | None = Field(None, alias="EQUIP_CODE")
    equip_name: str | None = Field(None, alias="EQUIP_NAME")
    utility_used: float | None = Field(None, alias="UTILITY_USED")

    model_config = {"from_attributes": True, "populate_by_name": True}
