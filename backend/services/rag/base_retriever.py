from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseRetriever(ABC):
    """Abstract base class interface for domain retrievers."""

    @abstractmethod
    def retrieve(self, query: str, **kwargs: Any) -> Dict[str, Any]:
        """Retrieve relevant context documents and structured information for a query.

        Returns:
            Dict containing retrieved_docs list and domain-specific metadata.
        """
        pass
