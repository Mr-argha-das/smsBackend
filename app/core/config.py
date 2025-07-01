# NEW ✅
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Literal
import os

class BaseAppSettings(BaseSettings):
    app_name: str = "ERP App"
    app_port: int = Field(..., env="APP_PORT")
    app_host: str = Field(..., env="APP_HOST")
    debug: bool = True
    environment: Literal["dev", "prod"] = Field("dev", env="ENVIRONMENT")
    
    mongo_uri: str = Field(..., env="MONGO_URI")
    mongo_db_name: str = Field(..., env="MONGO_DB_NAME")
    
    allowed_hosts: List[str] = ["*"]
    allowed_origins: List[str] = ["*"]

    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'dev')}"
