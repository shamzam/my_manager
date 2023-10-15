from fastapi import APIRouter, Depends

from routers.authentication import get_current_user
from models.usersModels import User, UserResponse, UserUpdateRequest
from functions.usersFuncs import register_user, update_user, delete_user

users_router = APIRouter(
    prefix="/users", dependencies=[Depends(get_current_user)], tags=["users"])


@users_router.post("/register", response_model=UserResponse)
def register_user_api(user: User):
    result = register_user(user)
    return UserResponse(data=result["data"], error_code=result["error_code"], error_detail=result["error_detail"])


@users_router.post("/update", response_model=UserResponse)
def update_user_api(user_update: UserUpdateRequest):
    result = update_user(user_update.user, user_update.former_user_id)
    return UserResponse(data=result["data"], error_code=result["error_code"], error_detail=result["error_detail"])


@users_router.post("/delete", response_model=UserResponse)
def delete_user_api(user: User):
    result = delete_user(user)
    return UserResponse(data=result["data"], error_code=result["error_code"], error_detail=result["error_detail"])
