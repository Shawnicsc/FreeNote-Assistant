from langchain_community.vectorstores import FAISS

from app.rag.embedding import get_embedding

"""build vectorstore from documents"""
def build_vectorstore(docs):
    embedding = get_embedding()
    return FAISS.from_documents(docs, embedding)

