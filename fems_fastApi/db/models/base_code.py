from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from fems_fastApi.db.base import Base


class BaseCode(Base):
    """Base code model for TB_BASE_CODE."""

    __tablename__ = "TB_BASE_CODE"
    __table_args__ = {"schema": "dbo"}

    main_code: Mapped[str] = mapped_column("MAIN_CODE", String(50), primary_key=True)
    sub_code: Mapped[str | None] = mapped_column("SUB_CODE", String(50), primary_key=True, nullable=True)
    code_name: Mapped[str | None] = mapped_column("CODE_NAME", String(100), nullable=True)
    code_lvl: Mapped[str | None] = mapped_column("CODE_LVL", String(10), nullable=True)
    ref_num1: Mapped[float | None] = mapped_column("REF_NUM1", Numeric(18, 4), nullable=True)
    ref_num2: Mapped[float | None] = mapped_column("REF_NUM2", Numeric(18, 4), nullable=True)
    ref_num3: Mapped[float | None] = mapped_column("REF_NUM3", Numeric(18, 4), nullable=True)
    ref_str1: Mapped[str | None] = mapped_column("REF_STR1", String(200), nullable=True)
    ref_str2: Mapped[str | None] = mapped_column("REF_STR2", String(200), nullable=True)
    ref_str3: Mapped[str | None] = mapped_column("REF_STR3", String(200), nullable=True)
    use_yn: Mapped[str | None] = mapped_column("USE_YN", String(1), nullable=True)
    remark: Mapped[str | None] = mapped_column("REMARK", String(500), nullable=True)
