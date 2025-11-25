import chromadb
from chromadb.utils import embedding_functions
import os

# Persist data in the project folder
DB_PATH = os.path.join(os.getcwd(), "chroma_db")

def get_client():
    return chromadb.PersistentClient(path=DB_PATH)

def get_collection():
    client = get_client()
    # Use default embedding function (all-MiniLM-L6-v2)
    # This downloads the model on first use.
    ef = embedding_functions.DefaultEmbeddingFunction()
    
    return client.get_or_create_collection(
        name="movie_plots",
        embedding_function=ef
    )

def add_movie_to_memory(title: str, overview: str, rating: int = None, genres: list = []):
    """
    Stores a movie's semantic meaning (plot) along with metadata.
    """
    collection = get_collection()
    
    # Create a rich text representation for embedding
    # We include genres to help with semantic matching
    document_text = f"{title}. {overview}. Genres: {', '.join(genres)}"
    
    # Metadata for filtering
    metadata = {
        "title": title,
        "rating": rating if rating is not None else -1,
        "genres": ", ".join(genres)
    }
    
    collection.upsert(
        documents=[document_text],
        metadatas=[metadata],
        ids=[str(abs(hash(title)))] # Simple deterministic ID
    )
    return f"Memorized '{title}' in vector database."

def search_similar_content(query: str, n_results: int = 5):
    """
    Finds movies in your database (or potentially pre-seeded ones) 
    that match the semantic meaning of the query.
    """
    collection = get_collection()
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    # Parse results
    matches = []
    if results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i]
            matches.append({
                "title": meta["title"],
                "match_score": 1, # Chroma distance is distinct, simplified here
                "overview": doc
            })
            
    return matches
