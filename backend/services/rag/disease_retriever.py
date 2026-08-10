from typing import Any, Dict
from backend.services.rag.base_retriever import BaseRetriever
from ai.disease_detection.scripts.retrieve_disease_knowledge import retrieve_disease_knowledge


class DiseaseRetriever(BaseRetriever):
    """Real retriever for Disease Detection & Recommendation RAG integration using ChromaDB."""

    def retrieve(self, query: str = "", **kwargs: Any) -> Dict[str, Any]:
        """Query disease ChromaDB collection using crop, disease, and search query."""
        crop_name = kwargs.get("crop_name") or ""
        disease_name = kwargs.get("disease_name") or ""
        top_k = kwargs.get("top_k") or 4

        retrieved_docs = retrieve_disease_knowledge(
            crop_name=crop_name,
            disease_name=disease_name,
            query=query,
            top_k=top_k
        )

        disease_status = f"{crop_name} — {disease_name}" if crop_name and disease_name else "Unknown Plant Disease"

        return {
            "disease_status": disease_status,
            "retrieved_docs": retrieved_docs,
        }
