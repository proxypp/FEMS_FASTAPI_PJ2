from decimal import Decimal

from pydantic import BaseModel, field_validator


class RealTimeEnergyEfficiencyResponse(BaseModel):
    """실시간 에너지 효율 조회 결과.

    금일/전일 'Kw' 사용량과 전일 대비 금일 사용량 비율(효율, %), 기준일자를 반환한다.
    """

    cur_utility_used: Decimal | None = None  # 금일 사용량
    be_utility_used: Decimal | None = None  # 전일 사용량
    efficiency: Decimal | None = None  # 전일 대비 금일 사용량 비율(%)
    utility_date: str | None = None  # 기준일자

    model_config = {"from_attributes": True}

    @field_validator("utility_date", mode="before")
    @classmethod
    def coerce_date(cls, v: object) -> str | None:
        # 프로시저는 UTILITY_DATE를 date 타입으로 반환하므로 문자열로 변환한다.
        if v is None:
            return None
        return str(v)
