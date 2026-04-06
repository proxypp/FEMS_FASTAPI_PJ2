from pydantic import BaseModel

class LoginRequest(BaseModel):
    """Login request schema."""

    user_id: str
    password: str

class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"
    user_id: str
    user_nm: str | None = None
    admin_yn: str | None = None

class LogoutRequest(BaseModel):
    """Logout request schema."""

    user_id: str


class RegisterRequest(BaseModel):
    """Register request schema."""

    user_id: str
    password: str
    user_nm: str | None = None
    email: str | None = None
    hp_no: str | None = None
    company: str | None = None

class RegisterResponse(BaseModel):
    """Register response schema."""

    user_id: str
    message: str = "Registration successful"