import os
from typing import Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.config import get_settings

settings = get_settings()

# 动态配置缓存，支持运行时修改
class AIConfigManager:
    _instance = None
    
    def __init__(self):
        self.api_key = settings.api_key
        self.base_url = settings.api_base_url
        self.model_id = settings.model_id
        self.embedding_model = "text-embedding-3-small" # 默认嵌入模型

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AIConfigManager()
        return cls._instance

    def update_config(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model_id: Optional[str] = None):
        if api_key: self.api_key = api_key
        if base_url: self.base_url = base_url
        if model_id: self.model_id = model_id

config_manager = AIConfigManager.get_instance()

def get_llm():
    return ChatOpenAI(
        api_key=config_manager.api_key,
        model=config_manager.model_id,
        base_url=config_manager.base_url,
        temperature=0,
    )

def get_embeddings():
    return OpenAIEmbeddings(
        api_key=config_manager.api_key,
        base_url=config_manager.base_url,
        model=config_manager.embedding_model
    )
