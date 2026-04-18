from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"


def ingest_documents() -> dict:
    if not DOCUMENTS_DIR.exists():
        return {
            "status": "error",
            "message": f"Documents folder not found: {DOCUMENTS_DIR}"
        }

    markdown_files = list(DOCUMENTS_DIR.glob("*.md"))

    if not markdown_files:
        return {
            "status": "error",
            "message": "No markdown files found in rag/documents"
        }

    documents = []

    for file_path in markdown_files:
        loader = TextLoader(str(file_path), encoding="utf-8")
        loaded_docs = loader.load()
        documents.extend(loaded_docs)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    split_docs = text_splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vectorstore = FAISS.from_documents(split_docs, embeddings)
    vectorstore.save_local(str(VECTORSTORE_DIR))

    return {
        "status": "success",
        "documents_loaded": len(documents),
        "chunks_created": len(split_docs),
        "vectorstore_path": str(VECTORSTORE_DIR)
    }


if __name__ == "__main__":
    result = ingest_documents()
    print(result)