from decimal import Decimal

from pydantic import BaseModel, field_validator

# 프로시저(USP_KPI_ITEM_PRODUCT_COST_SEARCH)의 한글 컬럼명 -> 응답 필드 매핑
COLUMN_MAP: dict[str, str] = {
    "제품코드": "item_code",
    "제품명": "item_name",
    "연도": "year",
    "1월": "m01",
    "2월": "m02",
    "3월": "m03",
    "4월": "m04",
    "5월": "m05",
    "6월": "m06",
    "7월": "m07",
    "8월": "m08",
    "9월": "m09",
    "10월": "m10",
    "11월": "m11",
    "12월": "m12",
    "연평균": "year_avg",
}

_DECIMAL_FIELDS = ("m01", "m02", "m03", "m04", "m05", "m06",
                   "m07", "m08", "m09", "m10", "m11", "m12", "year_avg")


class KpiItemProductCostResponse(BaseModel):
    """KPI 제품원가(절감률) 응답 스키마 (연도별 월간 단위원가와 연평균)."""

    item_code: str | None = None
    item_name: str | None = None
    year: str | None = None
    m01: float | None = None
    m02: float | None = None
    m03: float | None = None
    m04: float | None = None
    m05: float | None = None
    m06: float | None = None
    m07: float | None = None
    m08: float | None = None
    m09: float | None = None
    m10: float | None = None
    m11: float | None = None
    m12: float | None = None
    year_avg: float | None = None

    model_config = {"from_attributes": True}

    @field_validator("year", mode="before")
    @classmethod
    def coerce_year(cls, v: object) -> str | None:
        if v is None:
            return None
        return str(v)

    @field_validator(*_DECIMAL_FIELDS, mode="before")
    @classmethod
    def coerce_decimal(cls, v: object) -> float | None:
        if v is None:
            return None
        if isinstance(v, Decimal):
            return float(v)
        return v
