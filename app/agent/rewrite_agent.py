from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from app.core.llm_factory import get_llm


class RewriteAgent:
    def __init__(self):
        self.llm = get_llm()

        # 初始化 Jinja2 环境
        prompt_dir = Path(__file__).parent.parent / "prompt"
        self.env = Environment(
            loader=FileSystemLoader(prompt_dir),
            autoescape=False,
        )

    def _build_prompt(self, document_content: str) -> str:
        template = self.env.get_template("rewrite_prompt.jinja2")
        return template.render(document_content=document_content)

    def run(self, document_content: str) -> str:
        """
        执行总结任务

        :param document_content: Markdown 文档内容
        :return: JSON 字符串（结构化总结）
        """
        prompt = self._build_prompt(document_content)

        response = self.llm.invoke(prompt)

        return response.content