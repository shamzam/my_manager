from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    password: str
    username: str
    role: int
    email: str | None = None


class UserUpdateRequest(BaseModel):
    user: User
    former_user_id: str


class UserResponse(BaseModel):
    data: User | None = None
    error_code: int
    error_detail: str
