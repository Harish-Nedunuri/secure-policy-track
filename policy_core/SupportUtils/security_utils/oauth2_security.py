from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from policy_core.SupportUtils.secret_utils.config import Settings


class AuthService:
    """
    Authentication service class responsible for handling user authentication, 
    password verification, and JWT token creation.
    
    Attributes:
        SECRET_KEY (str): The secret key used to sign the JWT tokens.
        ALGORITHM (str): The algorithm used for JWT encoding.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Token expiration time in minutes for access tokens.
        REFRESH_TOKEN_EXPIRE_DAYS (int): Token expiration time in days for refresh tokens.
        pwd_context (CryptContext): A context handler for password hashing using bcrypt.
        oauth2Scheme (OAuth2PasswordBearer): OAuth2 password flow handler for token authentication.
        users_db (dict): A temporary in-memory database holding user credentials.
    """
    
    def __init__(self, settings: Settings):
        """
        Initializes the AuthService with security settings and prepares 
        encryption/hashing context for passwords.
        
        Args:
            settings (Settings): Configuration object containing secret key, algorithm,
                                 and token expiration settings.
        """
        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = settings.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

        # Validate algorithm on initialization
        self.validate_algorithm(self.ALGORITHM)

        # TODO: Do not hardcode user credentials; use a database.
        self.users_db = {
            "testusername": {
                "username": "testusername",
                "hashed_password": "$2b$12$RkrR366bUYjFfstvxkZH8eXBG6fGGDSDCjX3wB63N8Wa6eQm.vU2i"
            }
        }

    def validate_algorithm(self, algorithm: str) -> None:
        """
        Validates the algorithm used for JWT encoding and decoding to ensure it is secure.

        Args:
            algorithm (str): The algorithm provided in the settings.

        Raises:
            ValueError: If the algorithm is not secure or supported.
        """
        valid_algorithms = ['HS256', 'RS256']
        if algorithm not in valid_algorithms:
            raise ValueError(f"Insecure or unsupported algorithm: {algorithm}. Choose one of {valid_algorithms}.")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies if a plain text password matches the hashed password.

        Args:
            plain_password (str): The plain text password provided by the user.
            hashed_password (str): The hashed password stored in the database.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """
        Authenticates a user by verifying the username and password combination.

        Args:
            username (str): The username provided by the user.
            password (str): The plain text password provided by the user.

        Returns:
            Optional[dict]: User dictionary if authentication is successful, 
                            otherwise None.
        """
        user = self.users_db.get(username)
        if not user or not self.verify_password(password, user['hashed_password']):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Creates a signed JWT access token with an optional expiration time.

        Args:
            data (dict): The payload data to encode within the token.
            expires_delta (Optional[timedelta]): Optional expiration time for the token. 
                                                 Defaults to ACCESS_TOKEN_EXPIRE_MINUTES if not provided.

        Returns:
            str: The signed JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})

        # Ensure secure algorithm is used for encoding
        self.validate_algorithm(self.ALGORITHM)
        
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Creates a signed JWT refresh token with an optional expiration time.

        Args:
            data (dict): The payload data to encode within the token.
            expires_delta (Optional[timedelta]): Optional expiration time for the token. 
                                                 Defaults to REFRESH_TOKEN_EXPIRE_DAYS if not provided.

        Returns:
            str: The signed JWT refresh token.
        """
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode.update({"exp": expire})

        # Ensure secure algorithm is used for encoding
        self.validate_algorithm(self.ALGORITHM)
        
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
