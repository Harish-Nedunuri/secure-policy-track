import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file if it exisits in the project root
load_dotenv(dotenv_path=env_path) if (env_path := Path(".") / ".env").exists() else None

class Settings(BaseSettings):
    """
    Configure environment vairables as APP settings
    1. AUTHENTICATION & SECUIRTY
    2. DATABASE 

    """ 
    # 1. AUTHENTICATION & SECUIRTY
    DEBUG: bool = os.getenv('DEBUG')    
    SECRET_KEY: str = os.getenv('SECRET_KEY')   
    ALGORITHM: str = os.getenv('ALGORITHM',default='HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',default=15)
    REFRESH_TOKEN_EXPIRE_DAYS: int = os.getenv('REFRESH_TOKEN_EXPIRE_DAYS',default=7) 

    # 2. DATABASE
    POSTGRES_ADMIN_USER: str = os.getenv('POSTGRES_ADMIN_USER')   
    POSTGRES_ADMIN_PASSWORD: str = os.getenv('POSTGRES_ADMIN_PASSWORD')
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT: int = os.getenv('POSTGRES_PORT')
    POSTGRES_INSDB: str = os.getenv("POSTGRES_INSDB")

 


   
   
    
