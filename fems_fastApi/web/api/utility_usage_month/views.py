from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.db.models.utility_usage_month import UtilityUsageMonth
from fems_fastApi.web.api.utility_usage_month.schema import (
    UtilityUsageMonthRequest,
    UtilityUsageMonthResponse,
)

router = APIRouter()


@router.get("/max-id", response_model=int)
async def get_max_utility_usage_id(
    session: AsyncSession = Depends(get_db_session),
) -> int:
    """utility_usage_id의 최대값 조회."""
    result = await session.execute(select(func.max(UtilityUsageMonth.utility_usage_id)))
    return result.scalar() or 0


@router.get("", response_model=list[UtilityUsageMonthResponse])
async def get_utility_usage_month(
    bill_dt_from: str | None = Query(None, description="조회 시작일 (YYYYMMDD, 예: 20260313)"),
    bill_dt_to: str | None = Query(None, description="조회 종료일 (YYYYMMDD, 예: 20260320)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[UtilityUsageMonthResponse]:
    """월별 유틸리티 사용량 조회. bill_dt 범위 조건 선택 가능."""
    query = select(UtilityUsageMonth)

    if bill_dt_from and bill_dt_to:
        query = query.where(
            UtilityUsageMonth.bill_dt.between(bill_dt_from, bill_dt_to)
        )
    elif bill_dt_from or bill_dt_to:
        raise HTTPException(
            status_code=422,
            detail="bill_dt_from과 bill_dt_to 두 값을 모두 입력해주세요.",
        )

    result = await session.execute(query)
    rows = result.scalars().all()

    return [UtilityUsageMonthResponse.model_validate(row) for row in rows]


@router.post("/{utility_usage_id}", response_model=UtilityUsageMonthResponse, status_code=201)
async def create_utility_usage_month(
    utility_usage_id: int,
    body: UtilityUsageMonthRequest,
    session: AsyncSession = Depends(get_db_session),
) -> UtilityUsageMonthResponse:
    """월별 유틸리티 사용량 등록."""
    row = UtilityUsageMonth(utility_usage_id=utility_usage_id, **body.model_dump())
    session.add(row)
    await session.flush()

    return UtilityUsageMonthResponse.model_validate(row)


@router.delete("/{utility_usage_id}", status_code=204)
async def delete_utility_usage_month(
    utility_usage_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> None:
    """월별 유틸리티 사용량 삭제."""
    result = await session.execute(
        select(UtilityUsageMonth).where(UtilityUsageMonth.utility_usage_id == utility_usage_id)
    )
    row = result.scalar_one_or_none()

    if row is None:
        raise HTTPException(status_code=404, detail="해당 utility_usage_id가 존재하지 않습니다.")

    await session.delete(row)
    await session.flush()


@router.put("/{utility_usage_id}", response_model=UtilityUsageMonthResponse)
async def update_utility_usage_month(
    utility_usage_id: int,
    body: UtilityUsageMonthRequest,
    session: AsyncSession = Depends(get_db_session),
) -> UtilityUsageMonthResponse:
    """월별 유틸리티 사용량 수정."""
    result = await session.execute(
        select(UtilityUsageMonth).where(UtilityUsageMonth.utility_usage_id == utility_usage_id)
    )
    row = result.scalar_one_or_none()

    if row is None:
        raise HTTPException(status_code=404, detail="해당 utility_usage_id가 존재하지 않습니다.")

    for key, value in body.model_dump(exclude_none=True).items():
        setattr(row, key, value)

    await session.flush()

    return UtilityUsageMonthResponse.model_validate(row)
