from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.db.models.item import Item
from fems_fastApi.web.api.item.schema import ItemCreateRequest, ItemResponse, ItemUpdateRequest

router = APIRouter()


@router.get("", response_model=list[ItemResponse])
async def get_items(
    item_code: str = Query(default="", description="품목 코드 (부분 검색)"),
    item_name: str = Query(default="", description="품목명 (부분 검색)"),
    use_yn: str = Query(default="", description="사용여부 (Y: 사용중, N: 종료, 빈값: 전체)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[ItemResponse]:
    """품목 목록 조회 (ITEM_CODE/ITEM_NAME 부분 검색, ITEM_TYPE 정렬)."""
    query = select(Item).where(
        Item.item_code.like(f"%{item_code}%"),
        Item.item_name.like(f"%{item_name}%"),
    )

    if use_yn == "Y":
        query = query.where(or_(Item.end_dt == None, Item.end_dt == ""))  # noqa: E711
    elif use_yn == "N":
        query = query.where(and_(Item.end_dt != None, Item.end_dt != ""))  # noqa: E711

    query = query.order_by(Item.item_type)
    result = await session.execute(query)
    rows = result.scalars().all()

    return [ItemResponse.model_validate(row) for row in rows]


@router.post("", status_code=201)
async def create_item(
    body: ItemCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """품목 등록."""
    existing = await session.execute(
        select(Item).where(Item.item_code == body.item_code),
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="이미 존재하는 품목 코드입니다.")

    item = Item(
        mill_cd=body.mill_cd,
        item_code=body.item_code,
        item_name=body.item_name,
        item_type=body.item_type,
        item_wet=body.item_wet,
        start_dt=body.start_dt,
        end_dt=body.end_dt,
        grade=body.grade,
        color=body.color,
        remark=body.remark,
        cre_user=body.cre_user,
    )
    session.add(item)
    await session.commit()

    return {"message": "등록되었습니다.", "item_code": body.item_code}


@router.put("/{item_code}")
async def update_item(
    item_code: str,
    body: ItemUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """품목 수정 (ITEM_CODE 조건, UPD_DT는 현재 시간 자동 설정)."""
    result = await session.execute(
        select(Item).where(Item.item_code == item_code),
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="품목을 찾을 수 없습니다.")

    values = {k: v for k, v in body.model_dump().items() if v is not None}
    values["upd_dt"] = func.now()

    await session.execute(
        update(Item).where(Item.item_code == item_code).values(**values),
    )
    await session.commit()

    return {"message": "수정되었습니다.", "item_code": item_code}
