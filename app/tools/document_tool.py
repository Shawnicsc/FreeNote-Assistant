import os
from pathlib import Path
from dotenv import load_dotenv
from app.model.schema import Document, create_document, DocumentRequest

load_dotenv()

def show_document(document: Document) -> str:
    return f"Document ID: {document.document_id}\nTitle: {document.document_title}\nContent: {document.document_content}\nCreated At: {document.created_at}"

def read_document():
    results = []
    for md_file in Path(os.getenv("Local_File_Path")).glob("*.md"):
        text = parse_markdown(md_file)
        if text:
            document_request = DocumentRequest(
                document_title=text["title"],
                document_content=text["content"]
            )
            document = create_document(
                document_request
            )
            results.append(document)
    return results



def parse_markdown(md_path: Path):
    content = md_path.read_text(encoding="utf-8").strip()

    title = md_path.stem

    return {
        "title": title,
        "content": content
    }

if __name__ == "__main__":
    documents = read_document()
    for doc in documents:
        print(show_document(doc))