from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from app.core.llm_factory import get_llm


class BaseAgent:
    """
       BaseAgent
       - 所有 Agent 的基类
       - 负责 Prompt 加载、渲染和 LLM 调用
       """

    # 子类必须覆盖
    prompt_name: str | None = None

    def __init__(self):
        if not self.prompt_name:
            raise ValueError(
                f"{self.__class__.__name__} 必须指定 prompt_name"
            )

        self.llm = get_llm()

        prompt_dir = Path(__file__).parent.parent / "prompt"
        self.env = Environment(
            loader=FileSystemLoader(prompt_dir),
            autoescape=False,
        )

    def _build_prompt(self, document_content: str) -> str:
        """
        使用 Jinja2 渲染 Prompt
        """
        template = self.env.get_template(self.prompt_name)
        return template.render(document_content=document_content)

    def run(self, document_content: str) -> str:
        """
        Agent 统一执行入口
        """
        prompt = self._build_prompt(document_content)
        response = self.llm.invoke(prompt)
        return response.content