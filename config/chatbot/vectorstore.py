from langchain_chroma import Chroma
from .embeddings import get_embeddings

_vectorstore = None

def get_vectorstore():
    global _vectorstore

    if _vectorstore is None:
        print("⚡ Loading Chroma DB...")

        _vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=get_embeddings()  # lazy call
        )

    return _vectorstore