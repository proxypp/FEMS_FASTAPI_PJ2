from pydantic import BaseModel, Field


class EquipInspCompareResponse(BaseModel):
    """점검계획대비실적 메인 조회 결과 (PLAN_Dxx, ACT_Dxx 매핑)"""

    equip_code: str | None = Field(None, alias="EQUIP_CODE")
    equip_name: str | None = Field(None, alias="EQUIP_NAME")
    plan_yymm: str | None = Field(None, alias="PLAN_YYMM")

    # 1일 ~ 31일 계획/실적 필드 (SQL의 AS 명칭과 일치)
    plan_d01: str | None = Field(None, alias="PLAN_D01"); act_d01: str | None = Field(None, alias="ACT_D01")
    plan_d02: str | None = Field(None, alias="PLAN_D02"); act_d02: str | None = Field(None, alias="ACT_D02")
    plan_d03: str | None = Field(None, alias="PLAN_D03"); act_d03: str | None = Field(None, alias="ACT_D03")
    plan_d04: str | None = Field(None, alias="PLAN_D04"); act_d04: str | None = Field(None, alias="ACT_D04")
    plan_d05: str | None = Field(None, alias="PLAN_D05"); act_d05: str | None = Field(None, alias="ACT_D05")
    plan_d06: str | None = Field(None, alias="PLAN_D06"); act_d06: str | None = Field(None, alias="ACT_D06")
    plan_d07: str | None = Field(None, alias="PLAN_D07"); act_d07: str | None = Field(None, alias="ACT_D07")
    plan_d08: str | None = Field(None, alias="PLAN_D08"); act_d08: str | None = Field(None, alias="ACT_D08")
    plan_d09: str | None = Field(None, alias="PLAN_D09"); act_d09: str | None = Field(None, alias="ACT_D09")
    plan_d10: str | None = Field(None, alias="PLAN_D10"); act_d10: str | None = Field(None, alias="ACT_D10")
    plan_d11: str | None = Field(None, alias="PLAN_D11"); act_d11: str | None = Field(None, alias="ACT_D11")
    plan_d12: str | None = Field(None, alias="PLAN_D12"); act_d12: str | None = Field(None, alias="ACT_D12")
    plan_d13: str | None = Field(None, alias="PLAN_D13"); act_d13: str | None = Field(None, alias="ACT_D13")
    plan_d14: str | None = Field(None, alias="PLAN_D14"); act_d14: str | None = Field(None, alias="ACT_D14")
    plan_d15: str | None = Field(None, alias="PLAN_D15"); act_d15: str | None = Field(None, alias="ACT_D15")
    plan_d16: str | None = Field(None, alias="PLAN_D16"); act_d16: str | None = Field(None, alias="ACT_D16")
    plan_d17: str | None = Field(None, alias="PLAN_D17"); act_d17: str | None = Field(None, alias="ACT_D17")
    plan_d18: str | None = Field(None, alias="PLAN_D18"); act_d18: str | None = Field(None, alias="ACT_D18")
    plan_d19: str | None = Field(None, alias="PLAN_D19"); act_d19: str | None = Field(None, alias="ACT_D19")
    plan_d20: str | None = Field(None, alias="PLAN_D20"); act_d20: str | None = Field(None, alias="ACT_D20")
    plan_d21: str | None = Field(None, alias="PLAN_D21"); act_d21: str | None = Field(None, alias="ACT_D21")
    plan_d22: str | None = Field(None, alias="PLAN_D22"); act_d22: str | None = Field(None, alias="ACT_D22")
    plan_d23: str | None = Field(None, alias="PLAN_D23"); act_d23: str | None = Field(None, alias="ACT_D23")
    plan_d24: str | None = Field(None, alias="PLAN_D24"); act_d24: str | None = Field(None, alias="ACT_D24")
    plan_d25: str | None = Field(None, alias="PLAN_D25"); act_d25: str | None = Field(None, alias="ACT_D25")
    plan_d26: str | None = Field(None, alias="PLAN_D26"); act_d26: str | None = Field(None, alias="ACT_D26")
    plan_d27: str | None = Field(None, alias="PLAN_D27"); act_d27: str | None = Field(None, alias="ACT_D27")
    plan_d28: str | None = Field(None, alias="PLAN_D28"); act_d28: str | None = Field(None, alias="ACT_D28")
    plan_d29: str | None = Field(None, alias="PLAN_D29"); act_d29: str | None = Field(None, alias="ACT_D29")
    plan_d30: str | None = Field(None, alias="PLAN_D30"); act_d30: str | None = Field(None, alias="ACT_D30")
    plan_d31: str | None = Field(None, alias="PLAN_D31"); act_d31: str | None = Field(None, alias="ACT_D31")

    rate: int | None = Field(None, alias="RATE")

    model_config = {"from_attributes": True, "populate_by_name": True}


class EquipInspCompareSummaryResponse(BaseModel):
    """점검계획대비실적 요약 조회 결과 (USP_EQUIP_INSP_COMPARE - GRID_GBN='S', DML_GBN='S')."""

    total: int | None = Field(None, alias="TOTAL")
    done: int | None = Field(None, alias="DONE")
    miss: int | None = Field(None, alias="MISS")
    extra: int | None = Field(None, alias="EXTRA")

    model_config = {"from_attributes": True, "populate_by_name": True}
