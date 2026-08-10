from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "government_schemes"
TOP_K = 5

_model_cache: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    global _model_cache
    if _model_cache is None:
        _model_cache = SentenceTransformer(MODEL_NAME)
    return _model_cache


def retrieve_schemes(
    query: str,
    top_k: int = TOP_K,
    eligible_scheme_names: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Retrieve top-k semantically relevant government schemes from the existing ChromaDB collection.

    Args:
        query: Farmer natural language query or context description.
        top_k: Number of top relevant documents to return.
        eligible_scheme_names: Optional list of scheme names pre-filtered by eligibility criteria.

    Returns:
        List of dicts containing scheme_name, source_file, official_website, document_text, and distance.
    """
    base_dir = Path(__file__).resolve().parents[1]
    persist_dir = base_dir / "chroma_db"

    client = chromadb.PersistentClient(path=str(persist_dir))
    collection = client.get_collection(name=COLLECTION_NAME)

    model = get_embedding_model()
    query_embedding = model.encode(query, normalize_embeddings=True).tolist()

    where_clause = None
    if eligible_scheme_names:
        cleaned_names = [s.strip() for s in eligible_scheme_names if s and isinstance(s, str)]
        if len(cleaned_names) == 1:
            where_clause = {"scheme_name": cleaned_names[0]}
        elif len(cleaned_names) > 1:
            where_clause = {"scheme_name": {"$in": cleaned_names}}

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
                "scheme_name": metadata.get("scheme_name") or "",
                "source_file": metadata.get("source_file") or "",
                "official_website": metadata.get("official_website") or "",
                "document_text": doc or "",
                "distance": float(dist) if dist is not None else 0.0,
            }
        )

    return retrieved


def main() -> None:
    query = "I grow rice in Karnataka and need financial support for farming."
    results = retrieve_schemes(query, top_k=TOP_K)

    print(f"Query: {query}\n")
    for index, item in enumerate(results, start=1):
        print(f"{index}. {item['scheme_name']}")
        print(f"   Distance: {item['distance']:.4f}")
        print(f"   Source File: {item['source_file']}")
        print(f"   Website: {item['official_website'] or 'N/A'}")
        print(f"   Snippet: {item['document_text'][:120]}...\n")


if __name__ == "__main__":
    main()
