from typing import Dict, List, Tuple


class AIService:
    """
    PUBLIC_INTERFACE
    A minimal AI service abstraction to simulate GPT-like generation.
    In a real implementation, you would integrate with OpenAI, Azure OpenAI,
    Anthropic, or a local LLM via an SDK or HTTP.

    This mock uses simple template-based generation for demonstration.
    """

    # In-memory singleton-like storage for active model
    _active_model: str = "gpt-mini"
    _models: List[Dict[str, str]] = [
        {"name": "gpt-mini", "description": "Fast, concise model for short answers."},
        {"name": "gpt-balanced", "description": "Balanced performance for most FAQs."},
        {"name": "gpt-analytic", "description": "More detailed reasoning for complex queries."},
    ]

    def get_available_models(self) -> List[Dict[str, str]]:
        """Return available models."""
        return list(self._models)

    def get_active_model(self) -> str:
        """Return the currently active model."""
        return self._active_model

    def set_active_model(self, model_name: str) -> bool:
        """Set the active model if available. Returns True on success."""
        for m in self._models:
            if m["name"] == model_name:
                self._active_model = model_name
                return True
        return False

    def generate(self, prompt: str, context_snippets: List[Dict[str, str]]) -> Tuple[str, Dict]:
        """
        PUBLIC_INTERFACE
        Generate an answer given a prompt and context snippets.

        Returns:
            answer (str), meta (dict)
        """
        # Mock behavior varies slightly based on active model
        style_map = {
            "gpt-mini": "concise",
            "gpt-balanced": "balanced",
            "gpt-analytic": "analytical",
        }
        style = style_map.get(self._active_model, "balanced")

        # Build a simple answer using context. This is a stub.
        context_texts = [f"- {c.get('text', '')}" for c in context_snippets[:3]]
        joined_context = "\n".join(context_texts) if context_texts else "No context available."

        answer = (
            f"[{style.capitalize()} answer by {self._active_model}]\n"
            f"Question: {prompt}\n"
            f"Context considered:\n{joined_context}\n\n"
            "Answer: Based on the context above, here is a helpful response. "
            "For production, integrate a real LLM provider."
        )

        # Construct meta dictionary with consistent, simple typing
        tokens_estimate = len(prompt.split()) + sum(len(c.get('text', '').split()) for c in context_snippets)
        meta_out: Dict[str, object] = {
            "model": self._active_model,
            "tokens_estimate": tokens_estimate,
        }
        return answer, meta_out
