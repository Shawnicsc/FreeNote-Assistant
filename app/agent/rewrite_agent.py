from app.agent.base_agent import BaseAgent
from app.model.schema import RewriteResponse


class RewriteAgent(BaseAgent[RewriteResponse]):
    """
       RewriteAgent
       - 负责对文档内容进行改写
       - 继承自 BaseAgent，使用特定的改写 Prompt
       """

    prompt_name: str = "rewrite_prompt.jinja2"
    response_model = RewriteResponse