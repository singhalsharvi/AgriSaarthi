from typing import Any, Dict
from backend.services.rag.base_retriever import BaseRetriever


class DiseaseRetriever(BaseRetriever):
    """Clean placeholder retriever for Disease Detection & Recommendation RAG integration."""

    def retrieve(self, query: str = "", **kwargs: Any) -> Dict[str, Any]:
        """Placeholder retrieval for disease detection context."""
        evidence_text = (
            f"Disease Detection & Treatment (Placeholder Context):\n"
            f"Query: {query or 'General disease inquiry'}\n"
            f"Note: Disease detection vision model and vector index are undergoing integration."
        )

        retrieved_docs = [
            {
                "scheme_name": "Disease Identification Placeholder",
                "source_file": "ai/disease/placeholder",
                "official_website": "",
                "document_text": evidence_text,
                "distance": 0.0,
            }
        ]

        return {
            "disease_status": "placeholder",
            "retrieved_docs": retrieved_docs,
        }
