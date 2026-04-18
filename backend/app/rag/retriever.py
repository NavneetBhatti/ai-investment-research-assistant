from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


BASE_DIR = Path(__file__).resolve().parent
VECTORSTORE_DIR = BASE_DIR / "vectorstore"


def retrieve_context(query: str, k: int = 3) -> list[str]:
    if not VECTORSTORE_DIR.exists():
        return ["RAG vectorstore not found. Please run ingest.py first."]

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = vectorstore.similarity_search(query, k=k)

    if not docs:
        return ["No relevant RAG context found."]

    return [doc.page_content for doc in docs]