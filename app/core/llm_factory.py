from langchain_openai import ChatOpenAI

from app.config import get_settings

settings = get_settings()

# get llm instance
def get_llm():
    return ChatOpenAI(
        api_key=settings.api_key,
        model = settings.model_id,
        base_url= settings.api_base_url,
        temperature=0,
    )