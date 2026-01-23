from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

# load local config from .env
load_dotenv()

class Settings(BaseSettings):
    """ app settings"""
    app_name: str = "FreeNote-Assistant"
    app_version: str = "0.1.0"
    debug: bool = False

    """ sever settings"""
    host: str = "0.0.0.0"
    port: int = 8080

    """Cors settings"""
    cors_origins: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"

    log_level: str = "INFO"

settings = Settings()

def get_settings():
    """ get app settings """
    return settings