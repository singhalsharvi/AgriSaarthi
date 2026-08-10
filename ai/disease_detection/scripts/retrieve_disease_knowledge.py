from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "disease_knowledge"
_model_cache: Optional[SentenceTransformer] = None


def get_disease_embedding_model() -> SentenceTransformer:
    global _model_cache
    if _model_cache is None:
        _model_cache = SentenceTransformer(MODEL_NAME)
    return _model_cache


def retrieve_disease_knowledge(
    crop_name: str,
    disease_name: str,
    query: str = "",
    top_k: int = 4,
) -> List[Dict[str, Any]]:
    """Retrieve plant disease knowledge document sections from ChromaDB collection.

    Args:
        crop_name: E.g., 'Tomato', 'Pepper bell', 'Potato'
        disease_name: E.g., 'Early Blight', 'Late Blight', 'Bacterial Spot'
        query: Additional search query (optional)
        top_k: Number of documents to retrieve

    Returns:
        List of dicts containing metadata, content, and scores.
    """
    base_dir = Path(__file__).resolve().parents[1]
    persist_dir = base_dir / "chroma_db"

    client = chromadb.PersistentClient(path=str(persist_dir))
    collection = client.get_collection(name=COLLECTION_NAME)

    model = get_disease_embedding_model()
    
    # Construct query string
    search_text = f"{crop_name} {disease_name}".strip()
    if query and query.strip():
        search_text += f" {query.strip()}"
        
    query_embedding = model.encode(search_text, normalize_embeddings=True).tolist()

    # Formulate filter criteria to narrow down to this specific crop & disease if available
    # Matches case-insensitively or exactly depending on metadata
    where_clause = None
    if crop_name and disease_name:
        where_clause = {
            "$and": [
                {"crop": {"$eq": crop_name.strip()}},
                {"disease": {"$eq": disease_name.strip()}}
            ]
        }
    elif crop_name:
        where_clause = {"crop": {"$eq": crop_name.strip()}}

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause,
            include=["documents", "metadatas", "distances"],
        )
    except Exception:
        results = None

    documents = (results.get("documents", [[]])[0]) if results else []
    metadatas = (results.get("metadatas", [[]])[0]) if results else []
    distances = (results.get("distances", [[]])[0]) if results else []

    retrieved: List[Dict[str, Any]] = []
    for doc, metadata, dist in zip(documents, metadatas, distances):
        metadata = metadata or {}
        retrieved.append(
            {
                "scheme_name": f"Disease Knowledge: {metadata.get('crop')} - {metadata.get('disease')} ({metadata.get('section')})",
                "crop": metadata.get("crop") or "",
                "disease": metadata.get("disease") or "",
                "section": metadata.get("section") or "",
                "source_file": metadata.get("source") or "",
                "official_website": "",
                "document_text": doc or "",
                "distance": float(dist) if dist is not None else 0.0,
            }
        )

    # Fallback: if we filtered too aggressively and found nothing, query without crop/disease filters
    if not retrieved and where_clause is not None:
        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
            )
            documents = (results.get("documents", [[]])[0]) if results else []
            metadatas = (results.get("metadatas", [[]])[0]) if results else []
            distances = (results.get("distances", [[]])[0]) if results else []
            
            for doc, metadata, dist in zip(documents, metadatas, distances):
                metadata = metadata or {}
                retrieved.append(
                    {
                        "scheme_name": f"Disease Knowledge: {metadata.get('crop')} - {metadata.get('disease')} ({metadata.get('section')})",
                        "crop": metadata.get("crop") or "",
                        "disease": metadata.get("disease") or "",
                        "section": metadata.get("section") or "",
                        "source_file": metadata.get("source") or "",
                        "official_website": "",
                        "document_text": doc or "",
                        "distance": float(dist) if dist is not None else 0.0,
                    }
                )
        except Exception:
            pass

    return retrieved
