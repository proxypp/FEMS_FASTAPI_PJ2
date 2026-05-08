import io
from urllib.parse import quote

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.base_file.schema import BaseFileResponse

router = APIRouter()


@router.get("", response_model=list[BaseFileResponse])
async def get_base_files(
    file_id: str = Query(default="", description="파일 ID (부분 검색)"),
    file_name: str = Query(default="", description="파일명 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[BaseFileResponse]:
    """자료실 목록 조회 (USP_BASE_FILE - DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_FILE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@FILE_ID = :file_id, "
        "@FILE_NAME = :file_name"
    )
    result = await session.execute(sql, {"file_id": file_id, "file_name": file_name})
    rows = result.mappings().all()
    return [BaseFileResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.get("/{file_id}/download")
async def download_base_file(
    file_id: str,
    file_gbn: str = Query(default="", description="파일 구분"),
    session: AsyncSession = Depends(get_db_session),
) -> StreamingResponse:
    """자료실 파일 다운로드 (USP_BASE_FILE - DML_GBN='F')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_FILE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'F', "
        "@FILE_ID = :file_id, "
        "@FILE_GBN = :file_gbn"
    )
    result = await session.execute(sql, {"file_id": file_id, "file_gbn": file_gbn})
    raw = result.mappings().first()

    if not raw:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    row = {k.lower(): v for k, v in raw.items()}

    if row.get("file_bin") is None:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    file_bin: bytes = bytes(row["file_bin"])
    row_name: str = row.get("file_name") or "download"
    row_ext: str = row.get("file_ext") or ""
    filename = f"{row_name}.{row_ext}" if row_ext else row_name
    encoded_filename = quote(filename, encoding="utf-8")

    return StreamingResponse(
        io.BytesIO(file_bin),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"},
    )


@router.post("", status_code=201)
async def create_base_file(
    file_id: str = Form(..., description="파일 ID"),
    file_gbn: str = Form(..., description="파일 구분"),
    file_name: str = Form(..., description="파일명"),
    file_ext: str = Form(default="", description="파일 확장자"),
    user_id: str = Form(default="", description="등록자 ID"),
    file_bin: UploadFile | None = File(default=None, description="업로드 파일 (선택)"),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """자료실 파일 등록 (USP_BASE_FILE - DML_GBN='I')."""
    file_bin_data: bytes | None = None
    file_size: int = 0
    if file_bin and file_bin.filename:
        file_bin_data = await file_bin.read()
        file_size = len(file_bin_data)

    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_FILE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'I', "
        "@FILE_ID = :file_id, "
        "@FILE_GBN = :file_gbn, "
        "@FILE_NAME = :file_name, "
        "@FILE_EXT = :file_ext, "
        "@FILE_SIZE = :file_size, "
        "@FILE_BIN = :file_bin, "
        "@USER_ID = :user_id"
    )
    await session.execute(
        sql,
        {
            "file_id": file_id,
            "file_gbn": file_gbn,
            "file_name": file_name,
            "file_ext": file_ext,
            "file_size": file_size,
            "file_bin": file_bin_data,
            "user_id": user_id,
        },
    )
    await session.commit()
    return {"message": "파일이 등록되었습니다.", "file_id": file_id}


@router.put("/{file_id}")
async def update_base_file(
    file_id: str,
    file_gbn: str = Form(..., description="파일 구분"),
    file_name: str = Form(..., description="파일명"),
    file_ext: str = Form(default="", description="파일 확장자"),
    user_id: str = Form(default="", description="수정자 ID"),
    file_bin: UploadFile | None = File(default=None, description="업로드 파일 (선택)"),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """자료실 파일 수정 (USP_BASE_FILE - DML_GBN='U')."""
    file_bin_data: bytes | None = None
    file_size: int = 0
    if file_bin and file_bin.filename:
        file_bin_data = await file_bin.read()
        file_size = len(file_bin_data)

    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_FILE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'U', "
        "@FILE_ID = :file_id, "
        "@FILE_GBN = :file_gbn, "
        "@FILE_NAME = :file_name, "
        "@FILE_EXT = :file_ext, "
        "@FILE_SIZE = :file_size, "
        "@FILE_BIN = :file_bin, "
        "@USER_ID = :user_id"
    )
    await session.execute(
        sql,
        {
            "file_id": file_id,
            "file_gbn": file_gbn,
            "file_name": file_name,
            "file_ext": file_ext,
            "file_size": file_size,
            "file_bin": file_bin_data,
            "user_id": user_id,
        },
    )
    await session.commit()
    return {"message": "파일이 수정되었습니다.", "file_id": file_id}


@router.delete("/{file_id}")
async def delete_base_file(
    file_id: str,
    file_gbn: str = Query(..., description="파일 구분"),
    user_id: str = Query(default="", description="삭제자 ID"),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """자료실 파일 삭제 (USP_BASE_FILE - DML_GBN='D')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_FILE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'D', "
        "@FILE_ID = :file_id, "
        "@FILE_GBN = :file_gbn, "
        "@USER_ID = :user_id"
    )
    await session.execute(sql, {"file_id": file_id, "file_gbn": file_gbn, "user_id": user_id})
    await session.commit()
    return {"message": "파일이 삭제되었습니다."}
