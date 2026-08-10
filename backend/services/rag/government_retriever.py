from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai.government_schemes.scripts.filter_schemes import get_eligible_schemes
from ai.government_schemes.scripts.retrieve_schemes import retrieve_schemes
from backend.services.rag.base_retriever import BaseRetriever


class GovernmentSchemeRetriever(BaseRetriever):
    """RAG Retriever for Government Schemes combining profile eligibility filtering and ChromaDB vector retrieval."""

    def retrieve(
        self,
        query: str = "",
        top_k: int = 5,
        state: Optional[str] = None,
        crop: Optional[str] = None,
        farmer_category: Optional[str] = None,
        annual_income: Optional[float] = None,
        landholding: Optional[float] = None,
        age: Optional[float] = None,
        gender: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Execute eligibility filtering followed by semantic ChromaDB vector retrieval.

        Args:
            query: Farmer natural language query or context description.
            top_k: Number of relevant scheme documents to retrieve.
            state, crop, farmer_category, annual_income, landholding, age, gender: Farmer profile attributes.

        Returns:
            Dict containing 'eligible_schemes' (list of scheme names) and 'retrieved_docs' (list of doc dicts).
        """
        # Step 1: Rule-based eligibility filtering
        eligible_schemes = get_eligible_schemes(
            state=state,
            crop=crop,
            farmer_category=farmer_category,
            annual_income=annual_income,
            landholding=landholding,
            age=age,
            gender=gender,
            top_n=10,
        )

        # Step 2: Keep every supplied profile field in the semantic query.  This
        # lets the LLM/RAG layer explain recommendations against the actual inputs.
        profile_query = (
            f"Location: {state or 'India'}; annual income: {annual_income if annual_income is not None else 'not provided'} INR; "
            f"land size: {landholding if landholding is not None else 'not provided'} hectares; "
            f"gender: {gender or 'prefer not to say'}; farmer category: {farmer_category or 'not specified'}."
        )
        search_query = f"{query.strip()} {profile_query}" if query and query.strip() else f"Government schemes for farmers. {profile_query}"

        # Step 3: Semantic ChromaDB vector search
        retrieved_docs = retrieve_schemes(
            query=search_query,
            top_k=top_k,
            eligible_scheme_names=eligible_schemes,
        )

        return {
            "eligible_schemes": eligible_schemes,
            "retrieved_docs": retrieved_docs,
        }
