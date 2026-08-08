from pathlib import Path
from typing import Any, Dict, List

import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "government_schemes"
TOP_K = 5


def retrieve_schemes(query: str, top_k: int = TOP_K) -> List[Dict[str, Any]]:
    """Retrieve the top-k semantically relevant schemes from the existing collection."""
    base_dir = Path(__file__).resolve().parents[1]
    persist_dir = base_dir / "chroma_db"

    client = chromadb.PersistentClient(path=str(persist_dir))
    collection = client.get_collection(name=COLLECTION_NAME)

    stored = collection.get(include=["documents", "metadatas"])
    documents = stored.get("documents", []) or []
    metadatas = stored.get("metadatas", []) or []

    if not documents:
        return []

    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode(query, normalize_embeddings=True)
    document_embeddings = model.encode(documents, normalize_embeddings=True)
    similarity_scores = document_embeddings @ query_embedding

    retrieved: List[Dict[str, Any]] = []
    for doc, metadata, similarity in zip(documents, metadatas, similarity_scores):
        retrieved.append(
            {
                "scheme_name": (metadata or {}).get("scheme_name") or "",
                "document_text": doc or "",
                "official_website": (metadata or {}).get("official_website") or "",
                "distance": -float(similarity),
            }
        )

    retrieved.sort(key=lambda item: item["distance"])
    return retrieved[:top_k]


def main() -> None:
    query = "I grow rice in Karnataka and need financial support for farming."
    results = retrieve_schemes(query, top_k=TOP_K)

    print(f"Query: {query}\n")
    for index, item in enumerate(results, start=1):
        print(f"{index}. {item['scheme_name']}")
        print(f"   Distance: {item['distance']}")
        print(f"   Website: {item['official_website'] or 'N/A'}")
        print()


if __name__ == "__main__":
    main()
