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
            logger.info("Using local transformer fallback for generation")
            self.model_name = "gpt2"
            self.generator = pipeline(
                "text-generation",
                model=AutoModelForCausalLM.from_pretrained("gpt2"),
                tokenizer=AutoTokenizer.from_pretrained("gpt2"),
                device=-1,
                return_full_text=False,
            )

    def generate(self, prompt: str, max_tokens: int = 250) -> str:
        if self.use_openai:
            completion = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3,
            )
            return completion.choices[0].message.content.strip()

        response = self.generator(prompt, max_new_tokens=max_tokens, do_sample=False)
        text = response[0].get("generated_text", "")
        return text.strip()
