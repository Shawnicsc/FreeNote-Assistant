from app.agent.base_agent import BaseAgent


class SummaryAgent(BaseAgent):
    """
       SummaryAgent
       - 负责对文档内容进行总结
       - 继承自 BaseAgent，使用特定的总结 Prompt
       """

    prompt_name: str = "summary_prompt.jinja2"