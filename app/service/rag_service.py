import os

from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.config import get_settings
from app.core.llm_factory import get_llm, get_embeddings

settings = get_settings()

class RagService:
    def __init__(self):
        self.knowledge_base_path = settings.local_file_path
        self.vector_db = None
        self.embeddings = get_embeddings()
        self.llm = get_llm()

    def build_vector_store(self):
        """构建向量库"""
        if not os.path.exists(self.knowledge_base_path):
            return "指定的知识库路径不存在"
        
        # 加载所有 Markdown 文件
        loader = DirectoryLoader(self.knowledge_base_path, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
        docs = loader.load()
        
        if not docs:
            return "知识库目录下没有找到 Markdown 文件"

        # 向量化并存储
        self.vector_db = FAISS.from_documents(docs, self.embeddings)
        return "向量库构建成功"

    def query(self, question: str):
        """执行 RAG 查询"""
        if not self.vector_db:
            # 尝试实时构建（简单实现）
            status = self.build_vector_store()
            if self.vector_db is None:
                return f"无法执行查询: {status}"

        retriever = self.vector_db.as_retriever(search_kwargs={"k": 3})

        template = """你是一个专业的知识助手。请基于提供的【参考上下文】回答用户的【问题】。
        如果参考上下文中没有相关信息，请诚实地告诉用户你不知道，不要胡乱编造。

        【参考上下文】:
        {context}

        【问题】:
        {question}

        回答要求：使用 Markdown 格式，保持专业且简洁。
        """
        prompt = ChatPromptTemplate.from_template(template)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain.invoke(question)

rag_service = RagService()
