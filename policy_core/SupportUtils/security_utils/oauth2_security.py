from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from policy_core.SupportUtils.secret_utils.config import Settings


class AuthService:
    def __init__(self, settings: Settings):
        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = settings.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")
        #TODO: Do not  Hardcode user name and passwords
        self.users_db = {"testusername": {
            "username": "testusername",
            "hashed_password": "$2b$12$RkrR366bUYjFfstvxkZH8eXBG6fGGDSDCjX3wB63N8Wa6eQm.vU2i"}}   

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        user = self.users_db.get(username)
        if not user or not self.verify_password(password, user['hashed_password']):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
