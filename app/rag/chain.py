from langchain_classic.chains.retrieval_qa.base import RetrievalQA

"""build RAG chain"""
def build_rag_chain(llm, vectorstore):
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    return qa
