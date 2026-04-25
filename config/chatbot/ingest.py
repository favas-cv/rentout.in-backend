
# 22 products from PostgreSQL
#         ↓
# Converted to text paragraphs
#         ↓
# HuggingFace model converted each text → vector numbers
#         ↓
# All 22 vectors saved to ./chroma_db/ folder ✅

from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from django.db.models import  Count

from products.models import Product
from booking.models import Booked_items
from .embeddings import get_embeddings
import  os


def ingest_products():
    """
    Reads all active products from PostgreSQL,
    converts them to text, embeds them,
    and stores in ChromaDB vector database.
    """

    # ---- WHY: Get booking count per product ----
    # We count how many times each product was booked
    # so we can tell the AI "this product is popular"
    booking_counts = (
        Booked_items.objects
        .values('product_id')
        .annotate(total_bookings=Count('id'))
    )
    # Convert to a simple dict: { product_id: count }
    booking_map = {b['product_id']: b['total_bookings'] for b in booking_counts}

    # ---- WHY: Only active products ----
    products = Product.objects.select_related('category').all()
    print(f"Total products found: {products.count()}")
    print(f"Total bookings map: {len(booking_map)}")

    documents = []

    for product in products:
        bookings = booking_map.get(product.id, 0)

        # ---- WHY: Convert row to natural language ----
        # AI understands sentences, not table rows.
        # The richer the text, the better the search results.
        text = f"""
        Product: {product.title}
        Category: {product.category.category if product.category else 'N/A'}
        Brand: {product.brand_name or 'N/A'}
        Description: {product.description or 'N/A'}
        Material: {product.material or 'N/A'}
        Color: {product.color}
        Location: {product.locality or 'N/A'}
        Age: {product.age_years or 'N/A'} years old
        Price per day: ₹{product.price_per_day or 'N/A'}
        Monthly rent: ₹{product.monthly_rent or 'N/A'}
        Security deposit: ₹{product.security_deposit or 'N/A'}
        Minimum rental days: {product.min_rental_days}
        Times booked: {bookings} ({"popular" if bookings > 10 else "new"})
        """.strip()

        # ---- WHY: metadata ----
        # We store the product ID in metadata so later
        # we can return the actual product link/id to the user
        doc = Document(
            page_content=text,
            metadata={
                "product_id": product.id,
                "title": product.title,
                "price_per_day": str(product.price_per_day),
                "locality": product.locality or "",
            }
        )
        documents.append(doc)
        
    print(f"Total documents created: {len(documents)}")
    if len(documents) == 0:
        print("❌ No documents! Check if products exist and is_active=True")
        return

    # ✅ ADD THIS CHECK  
    print(f"Sample document:\n{documents[0].page_content}")


    # ---- WHY: HuggingFace Embeddings ----
    # This model converts text → vector numbers.
    # "all-MiniLM-L6-v2" is free, small, fast, runs locally.
    # No API cost for embedding.
    # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists("./chroma_db"):
        print("⚠️ DB already exists, skipping ingestion")
        return
    
    embeddings = get_embeddings() 

    # ---- WHY: Chroma ----
    # ChromaDB saves vectors to disk at ./chroma_db/
    # So you don't re-embed every time server restarts.
    # from_documents() embeds + saves in one step.
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    
    vectorstore.add_documents(documents)
    vectorstore.persist()
    
    # Chroma.from_documents(
    #     documents=documents,
    #     embedding=embeddings,
    #     persist_directory="./chroma_db"
    # )

    print(f"✅ Ingested {len(documents)} products into ChromaDB")


# Run this once from terminal:
# python manage.py shell -c "from chatbot.ingest import ingest_products; ingest_products()"
    