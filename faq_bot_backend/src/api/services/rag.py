from typing import List, Dict, Tuple
from .vector_store import InMemoryVectorStore
from .ai_service import AIService
from ..config.settings import Settings


class RagPipeline:
    """
    PUBLIC_INTERFACE
    Simple RAG pipeline that:
      1) Seeds an in-memory store with FAQ/document content.
      2) Retrieves relevant chunks by similarity.
      3) Calls AIService to generate a final answer.
    """

    def __init__(self, settings: Settings, ai_service: AIService):
        self.settings = settings
        self.ai_service = ai_service
        self.store = InMemoryVectorStore()
        self._seed_docs()

    def _seed_docs(self):
        # Seed with a few example FAQs and docs. In production, load from DB or files.
        docs = [
            ("How to reset my password?", "You can reset your password via the 'Forgot Password' link on the login page."),
            ("What is the refund policy?", "We offer a 30-day refund policy for unused services and unopened products."),
            ("How to contact support?", "Reach our support team via support@example.com or the help center chat."),
            ("Where can I view my invoices?", "Invoices are available in your account under Billing > Invoices."),
            ("Do you support SSO?", "Yes, SSO via SAML and OAuth2 is supported on enterprise plans."),
        ]
        for idx, (q, a) in enumerate(docs, start=1):
            self.store.add(text=f"Q: {q}\nA: {a}", source=f"seed_faq_{idx}")

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        results = self.store.search(query, top_k=top_k)
        contexts: List[Dict[str, str]] = []
        for doc, score in results:
            contexts.append({
                "source": doc["source"],
                "score": float(score),
                "text": doc["text"],
            })
        return contexts

    def generate_with_context(self, query: str, contexts: List[Dict[str, str]]) -> Tuple[str, Dict]:
        answer, meta = self.ai_service.generate(query, contexts)
        meta["context_count"] = len(contexts)
        return answer, meta
