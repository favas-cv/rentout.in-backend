# 🎓 What This File Does
# This is the brain of the chatbot:

# Takes user question
# Embeds the question → vector
# Searches ChromaDB for similar products
# Sends found products + question to Groq
# Returns natural language answer


# from .embeddings  import get_embeddings
from .vectorstore import get_vectorstore
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from django.conf import settings

# ---- WHY: Same embedding model as ingest.py ----
# MUST be the same model used during ingestion.
# If you change this, vectors won't match → wrong results
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# embeddings = get_embeddings()

# ---- WHY: Load existing ChromaDB from disk ----
# We already ingested 22 products into ./chroma_db/
# Here we just LOAD it — no re-embedding needed

# vectorstore = get_vectorstore()

# vectorstore = Chroma(
#     persist_directory="./chroma_db",
#     embedding_function=embeddings
# )

# ---- WHY: Groq LLM ----
# Groq is free and very fast
# It will receive the found products as context and answer naturally
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)

def ask(user_question: str) -> dict:
    """
    Full RAG flow:
    1. Embed user question
    2. Find similar products in ChromaDB
    3. Send context + question to Groq
    4. Return answer + matched products
    """
    vectorstore = get_vectorstore()
    

    # ---- WHY: similarity_search ----
    # This embeds the user question and finds
    # the 4 most similar product vectors in ChromaDB
    # matched_docs = vectorstore.similarity_search(user_question, k=4)
    
    retriever = vectorstore.as_retriever(search_kwargs={"k":4})
    matched_docs = retriever.invoke(user_question)

    if not matched_docs:
        return {"answer": "Sorry, we don't have that currently. Try another search. ."}

    # ---- WHY: Build context ----
    # We join all matched product texts into one block
    # This becomes the "knowledge" we give to Groq
    context = "\n\n".join([doc.page_content for doc in matched_docs])

    # ---- WHY: System message ----
    # This tells Groq WHO it is and HOW to behave
    # It sets the tone and rules for the chatbot
    system_prompt = """You are a rental assistant for Rentout.in in Kerala.
Help customers find products to rent.
Answer based ONLY on the product context provided.
Keep responses SHORT and CONCISE — maximum 3-4 lines.
Use simple language, no long paragraphs.
Mention product name, price per day and location only.
If not available say 'Sorry, we don't have that currently.'"""

    # ---- WHY: HumanMessage with context ----
    # We inject the found products INTO the user question
    # So Groq answers based on YOUR data, not its training data
    user_prompt = f"""Customer question: {user_question}

Available products context:
{context}

Please help the customer based on the above products."""

    # ---- WHY: invoke ----
    # Send messages to Groq and get response
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])

    # ---- WHY: metadata ----
    # Return product IDs too so frontend can show product cards
    matched_products = [
        {
            "product_id": doc.metadata.get("product_id"),
            "title": doc.metadata.get("title"),
            "price_per_day": doc.metadata.get("price_per_day"),
            "locality": doc.metadata.get("locality"),
        }
        for doc in matched_docs
    ]

    return {
        "answer": response.content,
        "matched_products": matched_products
    }