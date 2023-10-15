from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from models.usersModels import User
from functions.usersFuncs import login
from common.configUtils import read_config

# to get a string like this run:
# openssl rand -hex 32


class AuthConfig:
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


class Token(BaseModel):
    access_token: str
    token_type: str
    data: User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_config = AuthConfig()
read_config(auth_config, "./my_manager.ini", "auth")

auth_router = APIRouter(tags=["auth"])


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_config.SECRET_KEY,
                             algorithms=[auth_config.ALGORITHM])
        user: str = payload.get("data")
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = login(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=int(auth_config.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"data": user}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "data": user}
