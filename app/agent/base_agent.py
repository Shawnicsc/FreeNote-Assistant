from pathlib import Path
from typing import Any, Generic, TypeVar
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.core.llm_factory import get_llm

T = TypeVar("T", bound=BaseModel)

class BaseAgent(Generic[T]):
    """
    BaseAgent
    - 基类
    - 负责 Prompt 模板加载和 LCEL 链式调用
    """

    prompt_name: str | None = None
    response_model: type[T] | None = None

    def __init__(self):
        if not self.prompt_name:
            raise ValueError(f"{self.__class__.__name__} 必须指定 prompt_name")
        
        self.llm = get_llm()
        
        # 加载 Prompt 模板
        prompt_path = Path(__file__).parent.parent / "prompt" / self.prompt_name
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_content = f.read()
            
        self.prompt_template = ChatPromptTemplate.from_template(
            template_content, 
            template_format="jinja2"
        )
        self.output_parser = JsonOutputParser()
        
        # 构建 LCEL 链
        self.chain = self.prompt_template | self.llm | self.output_parser

    def run(self, document_content: str) -> T:
        """
        使用 LangChain 执行链式调用
        """
        return self.chain.invoke({"document_content": document_content})