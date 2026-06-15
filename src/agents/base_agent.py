"""
Base Agent - Clasa de baza pentru toti agentii din aplicatie.
Defineste interfata comuna si logica de comunicare cu Groq API.
"""

import json
import os
import re
import logging
from abc import ABC, abstractmethod
from typing import Optional


logger = logging.getLogger(__name__)


class BaseAgent(ABC):

    def __init__(self, model: str = "llama3-8b-8192", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature
        self.name = self.__class__.__name__

    def _call_ollama(self, system_prompt: str, user_message: str) -> str:
        """
        Apeleaza Groq API si returneaza raspunsul ca string.
        Numele metodei e pastrat _call_ollama pentru compatibilitate.
        """
        from groq import Groq

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ConnectionError(
                f"[{self.name}] GROQ_API_KEY lipseste din .env. "
                "Creeaza cont gratuit pe https://console.groq.com si adauga cheia in .env"
            )

        client = Groq(api_key=api_key)

        import time

        MAX_RETRIES = 2
        RATE_LIMIT_WAIT = 65  # seconds — enough for the 1-minute TPM window to reset

        for attempt in range(MAX_RETRIES + 1):
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message},
                    ],
                    temperature=self.temperature,
                    max_tokens=1200,
                    response_format={"type": "json_object"},
                )
                return response.choices[0].message.content.strip()

            except Exception as e:
                err_str = str(e)
                is_rate_limit = (
                    "429" in err_str
                    or "rate_limit" in err_str.lower()
                    or "rate limit" in err_str.lower()
                    or "tokens per minute" in err_str.lower()
                )
                if is_rate_limit and attempt < MAX_RETRIES:
                    logger.warning(
                        f"[{self.name}] Rate limit hit (attempt {attempt + 1}/{MAX_RETRIES + 1}). "
                        f"Waiting {RATE_LIMIT_WAIT}s..."
                    )
                    time.sleep(RATE_LIMIT_WAIT)
                    continue
                raise RuntimeError(f"[{self.name}] Groq API error: {err_str}")

    def _safe_parse_json(self, text: str) -> Optional[dict]:
        # 1. Parse direct
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 2. Extrage din bloc markdown ```json ... ```
        json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # 3. Extrage primul obiect JSON din text
        brace_match = re.search(r"\{.*\}", text, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group(0))
            except json.JSONDecodeError:
                pass

        return None

    @abstractmethod
    def run(self, input_data: str) -> dict:
        pass

    def __repr__(self):
        return f"{self.name}(model={self.model}, temperature={self.temperature})"