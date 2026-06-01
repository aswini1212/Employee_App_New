from pydantic import BaseModel

from models.employee import EmployeeRole


class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token:str
    refresh_token: str
    token_type:str = "bearer"

class TokenPayload(BaseModel):
    """Decoded JWT payload."""
    id: int
    email: str
    role: EmployeeRole

class TokenRefresh(BaseModel):
    refresh_token:str