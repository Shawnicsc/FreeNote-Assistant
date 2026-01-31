import json
from pathlib import Path
from app.agent.base_agent import BaseAgent
from app.model.schema import UmlResponse, UmlIR
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class UmlAgent(BaseAgent[UmlResponse]):
    """
    UmlAgent (Two-Stage Architecture)
    - Stage 1: UML Semantic Extraction (Markdown -> IR)
    - Stage 2: UML Rendering (IR -> Mermaid Source)
    """

    prompt_name: str = "uml_extraction_prompt.jinja2"
    render_prompt_name: str = "uml_render_prompt.jinja2"
    response_model = UmlResponse

    def __init__(self):
        # 初始化 Stage 1 (抽取)
        super().__init__()
        
        # 初始化 Stage 2 (渲染)
        render_prompt_path = Path(__file__).parent.parent / "prompt" / self.render_prompt_name
        with open(render_prompt_path, "r", encoding="utf-8") as f:
            render_template_content = f.read()
            
        self.render_prompt_template = ChatPromptTemplate.from_template(
            render_template_content,
            template_format="jinja2"
        )

        @tool
        def render_uml_tool(uml_code: str, uml_type: str, description: str):
            """将 UML IR 渲染为 Mermaid 源码。"""
            return {
                "uml_code": uml_code,
                "uml_type": uml_type,
                "description": description
            }

        self.render_tools = [render_uml_tool]
        self.render_llm = self.llm.bind_tools(self.render_tools, tool_choice="render_uml_tool")
        
        # Stage 1 Chain: Markdown -> IR (JSON)
        self.extraction_chain = self.prompt_template | self.llm | JsonOutputParser()
        
        # Stage 2 Chain: IR -> UmlResponse (Tool Call)
        self.render_chain = self.render_prompt_template | self.render_llm

    def run(self, document_content: str) -> UmlResponse:
        """
        执行两阶段流程
        """
        # --- Stage 1: Extraction ---
        uml_ir_dict = self.extraction_chain.invoke({"document_content": document_content})
        
        # --- Stage 2: Rendering ---
        # 将 IR 字典转为 JSON 字符串传递给渲染 Agent
        render_response = self.render_chain.invoke({"uml_ir": json.dumps(uml_ir_dict, ensure_ascii=False)})
        
        if render_response.tool_calls:
            args = render_response.tool_calls[0]["args"]
            return UmlResponse(**args)
        
        raise ValueError("UML 渲染阶段未能触发 Tool Call")
