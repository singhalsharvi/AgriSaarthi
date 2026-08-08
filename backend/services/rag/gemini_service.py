import logging
import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# Automatically load environment variables from .env file if present
load_dotenv()

LOG = logging.getLogger("gemini_service")

SYSTEM_PROMPT = """You are an expert AI Agricultural Assistant dedicated to empowering Indian farmers with clear, practical, and evidence-grounded advice.

STRICT GUIDELINES:
1. Answer using ONLY the supplied retrieved context and structured information.
2. Do NOT invent, hallucinate, or assume any facts about government schemes, crops, or diseases that are not explicitly present in the retrieved evidence.
3. If the retrieved context is insufficient or lacks specific answers, explicitly state that details are limited based on available data.
4. Clearly distinguish between Crop Recommendations, Disease Information, and Government Scheme eligibility/benefits.
5. For Crop Recommendations: Explain WHY each of the recommended crops is suitable for the farmer's soil and weather parameters (N, P, K, temperature, humidity, pH, rainfall), and detail their fertilizer, irrigation, and cultivation requirements using the retrieved agronomic context.
6. Provide practical, empathetic, and easily understandable guidance formatted with clear markdown headings and bullet points.
"""


class GeminiService:
    """Common Gemini LLM service for synthesizing final evidence-grounded answers for farmers."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = None
        self._sdk_type = None
        self._init_client()

    def _init_client(self) -> None:
        if not self.api_key:
            LOG.warning("GEMINI_API_KEY is not set. Operating in fallback synthesis mode.")
            return

        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
            self._sdk_type = "google-genai"
            LOG.info("Gemini initialized using 'google-genai' SDK.")
        except Exception as e1:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel("gemini-2.5-flash")
                self._sdk_type = "google-generativeai"
                LOG.info("Gemini initialized using legacy 'google.generativeai' SDK.")
            except Exception as e2:
                LOG.error("Failed to initialize Gemini SDK (%s / %s). Falling back.", e1, e2)
                self.client = None

    def generate_response(
        self,
        user_query: str,
        domain: str,
        retrieved_docs: List[Dict[str, Any]],
        structured_metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Synthesize a final evidence-grounded natural-language response using Gemini.

        Args:
            user_query: Farmer's original question or intent.
            domain: Target domain ('government_schemes', 'crop_recommendation', 'disease_detection').
            retrieved_docs: List of evidence document dicts from RAG retrieval.
            structured_metadata: Additional structured profile or ML prediction metadata.

        Returns:
            Synthesized markdown response string.
        """
        context_blocks = []
        for idx, doc in enumerate(retrieved_docs, start=1):
            name = doc.get("scheme_name") or "Document"
            site = doc.get("official_website") or "N/A"
            source = doc.get("source_file") or "N/A"
            content = doc.get("document_text") or ""
            context_blocks.append(
                f"=== Context Item {idx} ===\n"
                f"Title: {name}\n"
                f"Source File: {source}\n"
                f"Official Website: {site}\n"
                f"Content:\n{content}\n"
            )

        context_text = "\n".join(context_blocks) if context_blocks else "No relevant context retrieved."
        meta_text = str(structured_metadata) if structured_metadata else "None"

        user_prompt = (
            f"DOMAIN: {domain}\n"
            f"FARMER QUERY: {user_query or 'General query based on inputs'}\n"
            f"STRUCTURED METADATA: {meta_text}\n\n"
            f"RETRIEVED EVIDENCE CONTEXT:\n{context_text}\n\n"
            f"Synthesize a clear, empathetic, and evidence-grounded response for the farmer."
        )

        if not self.client:
            return self._generate_fallback_response(domain, user_query, retrieved_docs, structured_metadata)

        try:
            if self._sdk_type == "google-genai":
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[SYSTEM_PROMPT, user_prompt],
                )
                return response.text
            else:
                response = self.client.generate_content(f"{SYSTEM_PROMPT}\n\n{user_prompt}")
                return response.text
        except Exception as exc:
            LOG.error("Gemini API generation error: %s. Using fallback response.", exc)
            return self._generate_fallback_response(domain, user_query, retrieved_docs, structured_metadata)

    def _generate_fallback_response(
        self,
        domain: str,
        user_query: str,
        retrieved_docs: List[Dict[str, Any]],
        structured_metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Structured fallback synthesis when GEMINI_API_KEY is not available."""
        if domain == "government_schemes":
            scheme_items = []
            for doc in retrieved_docs:
                name = doc.get("scheme_name") or "Government Scheme"
                site = doc.get("official_website")
                site_info = f" — [Official Website]({site})" if site else ""
                snippet = doc.get("document_text", "").strip().split("\n")[0]
                scheme_items.append(f"### {name}{site_info}\n{snippet}")

            body = "\n\n".join(scheme_items) if scheme_items else "No eligible schemes found for the given criteria."
            return (
                f"## Recommended Government Schemes\n\n"
                f"Based on your profile eligibility and inquiry (*\"{user_query or 'Scheme Match'}\"*), here are the top matching government schemes:\n\n"
                f"{body}\n\n"
                f"> **Note**: Set `GEMINI_API_KEY` in `.env` file to enable full AI-synthesized custom advice."
            )
        elif domain == "crop_recommendation":
            preds = (structured_metadata or {}).get("predictions", {}).get("top_3_predictions", [])
            items = [f"1. **{p.get('crop', '').capitalize()}** ({p.get('confidence_score', 0)*100:.1f}% confidence)" for p in preds]
            crops_str = "\n".join(items) if items else "N/A"

            knowledge_blocks = []
            for doc in retrieved_docs:
                if doc.get("scheme_name", "").startswith("Crop Knowledge:"):
                    title = doc.get("scheme_name")
                    text = doc.get("document_text", "")
                    knowledge_blocks.append(f"### {title}\n{text}")

            kb_str = "\n\n".join(knowledge_blocks)
            return (
                f"## Crop Recommendation Analysis\n\n"
                f"Based on your soil and environmental inputs, the recommended crops are:\n\n"
                f"{crops_str}\n\n"
                f"## Agronomic Knowledge & Cultivation Requirements\n\n"
                f"{kb_str}\n\n"
                f"> **Note**: Set `GEMINI_API_KEY` in `.env` file to enable full AI-synthesized custom advice."
            )
        else:
            return f"Retrieved {len(retrieved_docs)} context documents for '{domain}'."
