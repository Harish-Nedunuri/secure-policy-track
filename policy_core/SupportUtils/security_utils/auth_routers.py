from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import  timedelta
from typing import Optional
from fastapi.routing import APIRouter
from typing import Any
from policy_core.SupportUtils.secret_utils.config import Settings
from policy_core.SupportUtils.security_utils.oauth2_security import AuthService

class Token(BaseModel):
    access_token: str
    access_token_expires_mins: Any
    token_type: str
    refresh_token_expires_days: Any
    refresh_token: Optional[str] = None

auth_ser = AuthService(Settings())
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    tags=["Authentication"],
    responses={404: {"description": "Not found"}}
)
@router.post("/token", response_model=Token, description="Provide credentials to acquire access-token")
async def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    username = form_data.username
    password = form_data.password
    
    user = auth_ser.authenticate_user(username, password)
    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth_ser.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_ser.create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=auth_ser.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = auth_ser.create_refresh_token(
        data={"sub": username}, expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "access_token_expires_mins": auth_ser.ACCESS_TOKEN_EXPIRE_MINUTES, "token_type": "bearer", "refresh_token": refresh_token, "refresh_token_expires_days": auth_ser.REFRESH_TOKEN_EXPIRE_DAYS}

router_refresh = APIRouter(
    tags=["Authentication"],
    responses={404: {"description": "Not found"}}
)
@router_refresh.post("/refresh-token", description="Refresh an access token")
async def refresh_access_token(
    refresh_token: str = Form(...)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(refresh_token, auth_ser.SECRET_KEY, algorithms=[auth_ser.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    access_token_expires = timedelta(minutes=auth_ser.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_ser.create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

router_success = APIRouter(
    tags=["Authentication"],
    responses={404: {"description": "Not found"}}
)
@router_success.get("/success-endpoint",description="An secure endpoint for greeting user")
async def auth_success_endpoint(token: str = Depends(oauth2Scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_ser.SECRET_KEY, algorithms=[auth_ser.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return {"message": f"Hello, {username}! Your access is granted."}

