from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    TESTING: bool = False
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
