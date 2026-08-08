from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "crop_knowledge"
_model_cache: Optional[SentenceTransformer] = None


def get_crop_embedding_model() -> SentenceTransformer:
    global _model_cache
    if _model_cache is None:
        _model_cache = SentenceTransformer(MODEL_NAME)
    return _model_cache


def retrieve_crop_knowledge(
    crop_names: List[str],
    query: str = "",
    top_k: int = 3,
) -> List[Dict[str, Any]]:
    """Retrieve agronomic knowledge documents for specified crop names from the Crop ChromaDB collection.

    Args:
        crop_names: List of crop names recommended by the ML model (e.g. ['rice', 'jute', 'maize']).
        query: Optional user query string.
        top_k: Max documents to return.

    Returns:
        List of dicts containing crop_name, title, source_file, and document_text.
    """
    base_dir = Path(__file__).resolve().parents[1]
    persist_dir = base_dir / "chroma_db"

    client = chromadb.PersistentClient(path=str(persist_dir))
    collection = client.get_collection(name=COLLECTION_NAME)

    model = get_crop_embedding_model()
    search_text = query.strip() if query and query.strip() else f"Agronomic requirements for {', '.join(crop_names)}"
    query_embedding = model.encode(search_text, normalize_embeddings=True).tolist()

    # Clean crop names for matching
    cleaned_crops = [c.lower().strip() for c in crop_names if c and isinstance(c, str)]

    where_clause = None
    if cleaned_crops:
        if len(cleaned_crops) == 1:
            where_clause = {"crop_name": cleaned_crops[0]}
        else:
            where_clause = {"crop_name": {"$in": cleaned_crops}}

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

    # Fallback to direct id lookup if where vector query returns fewer docs
    if len(documents) < len(cleaned_crops):
        try:
            get_res = collection.get(ids=cleaned_crops, include=["documents", "metadatas"])
            get_docs = get_res.get("documents", []) or []
            get_metas = get_res.get("metadatas", []) or []
            for doc, meta in zip(get_docs, get_metas):
                c_name = (meta or {}).get("crop_name", "")
                if c_name not in [m.get("crop_name") for m in metadatas if m]:
                    documents.append(doc)
                    metadatas.append(meta)
                    distances.append(0.0)
        except Exception:
            pass

    retrieved: List[Dict[str, Any]] = []
    for doc, metadata, dist in zip(documents, metadatas, distances):
        metadata = metadata or {}
        retrieved.append(
            {
                "scheme_name": f"Crop Knowledge: {metadata.get('title') or metadata.get('crop_name') or 'Crop'}",
                "crop_name": metadata.get("crop_name") or "",
                "source_file": metadata.get("source_file") or "",
                "official_website": "",
                "document_text": doc or "",
                "distance": float(dist) if dist is not None else 0.0,
            }
        )

    return retrieved
