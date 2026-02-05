from langchain_community.document_loaders import TextLoader, DirectoryLoader

"""load markdown documents from directory"""
def load_markdown_docs(path: str) :
    loader = DirectoryLoader(path,
                             glob="**/*.md",
                             loader_cls=TextLoader,
                             loader_kwargs={"encoding": "utf-8"}
                             )
    return loader.load()
