from langchain_huggingface import HuggingFaceEmbeddings

from app.core.llm_factory import settings

"""get huggingface embedding model"""
def get_embedding():
    return HuggingFaceEmbeddings(
        model_name = settings.embedding_model,
        model_kwargs = {'device': 'cpu'},
        encode_kwargs = {'normalize_embeddings': True}
    )
