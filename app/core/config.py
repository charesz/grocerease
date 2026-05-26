from pydantic_settings import BaseSettings
 
 
class Settings(BaseSettings):
    APP_NAME: str = "GrocerEase"
    DEBUG: bool = True
 
    MAIN_DATABASE_URL: str
    REPORTING_DATABASE_URL: str
 
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
 
    class Config:
        env_file = ".env"
 
 
settings = Settings()
