import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

# load local config from .env
load_dotenv()


# 然后尝试加载HelloAgents的.env(如果存在)
helloagents_env = Path(__file__).parent.parent.parent.parent / "HelloAgents" / ".env"
if helloagents_env.exists():
    load_dotenv(helloagents_env, override=False)  # 不覆盖已有的环境变量

class Settings(BaseSettings):
    """ app settings"""
    app_name: str = "FreeNote-Assistant"
    app_version: str = "0.1.0"
    debug: bool = False

    """ sever settings"""
    host: str = "0.0.0.0"
    port: int = 8000

    """Cors settings"""
    cors_origins: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"

    log_level: str = "INFO"

    """ LLM Settings"""
    api_key : str = os.getenv("LLM_API_KEY")
    model_id : str = os.getenv("LLM_MODEL_ID", "gpt-3.5-turbo")
    api_base_url : str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")

settings = Settings()

def get_settings():
    """ get app settings """
    return settings