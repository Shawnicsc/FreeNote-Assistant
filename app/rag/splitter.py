from langchain_text_splitters import RecursiveCharacterTextSplitter

"""split documents into smaller chunks"""
def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.split_documents(docs)