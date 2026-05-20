import os
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

class LlmService:
    def __init__(self):
        self.use_openai = bool(settings.openai_api_key) and OPENAI_AVAILABLE
        if self.use_openai:
            openai.api_key = settings.openai_api_key
            logger.info("Using OpenAI for generation")
            self.model_name = settings.llm_model
        else:
            # Render containers commonly run with tight memory limits.
            # Loading a local transformer (e.g. gpt2) can trigger large model downloads
            # and cause OOM during startup.
            #
            # We therefore do NOT load the local model unless explicitly enabled.
            logger.info(
                "OPENAI_API_KEY not set and OPENAI SDK not available; local transformer fallback is disabled"
            )
            self.model_name = settings.llm_model
            self.generator = None


    def generate(self, prompt: str, max_tokens: int = 250) -> str:
        if self.use_openai:
            completion = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3,
            )
            return completion.choices[0].message.content.strip()

        if self.generator is None:
            return (
                "Model is not available on this deployment. "
                "Set OPENAI_API_KEY to enable generation."
            )

        response = self.generator(prompt, max_new_tokens=max_tokens, do_sample=False)
        text = response[0].get("generated_text", "")
        return text.strip()

