"""
Base Agent - Clasa de bază pentru toți agenții din aplicație.
Definește interfața comună și logica de comunicare cu Ollama.
"""

import json
import requests
from abc import ABC, abstractmethod
from typing import Optional


OLLAMA_BASE_URL = "http://localhost:11434"


class BaseAgent(ABC):
    """
    Clasa de bază abstractă pentru agenții AI.
    Toți agenții moștenesc această clasă și implementează metoda `run`.
    """

    def __init__(self, model: str = "llama3", temperature: float = 0.7):
        """
        Args:
            model: Modelul Ollama de folosit (ex: 'llama3', 'mistral', 'phi3')
            temperature: Creativitatea răspunsului (0.0 = determinist, 1.0 = creativ)
        """
        self.model = model
        self.temperature = temperature
        self.name = self.__class__.__name__

    def _call_ollama(self, system_prompt: str, user_message: str) -> str:
        """
        Apelează Ollama API și returnează răspunsul ca string.

        Args:
            system_prompt: Instrucțiunile pentru comportamentul agentului
            user_message: Mesajul/input-ul de procesat

        Returns:
            Răspunsul modelului ca string

        Raises:
            ConnectionError: Dacă Ollama nu rulează local
            RuntimeError: Dacă modelul returnează o eroare
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": 1024,
                "num_ctx": 4096
            },
        }

        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json=payload,
                timeout=300,  # 2 minute timeout pentru modele locale
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"].strip()

        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"[{self.name}] Nu pot conecta la Ollama. "
                "Asigurați-vă că Ollama rulează: `ollama serve`"
            )
        except requests.exceptions.Timeout:
            raise RuntimeError(
                f"[{self.name}] Timeout - modelul '{self.model}' a depășit 120s. "
                "Încercați un model mai mic."
            )
        except KeyError:
            raise RuntimeError(
                f"[{self.name}] Răspuns neașteptat de la Ollama: {response.text[:200]}"
            )

    def _safe_parse_json(self, text: str) -> Optional[dict]:
        """
        Încearcă să parseze JSON din textul modelului.
        Modelele locale adesea adaugă text înainte/după JSON.

        Args:
            text: Textul brut de la model

        Returns:
            Dict cu datele parsate sau None dacă parsing-ul eșuează
        """
        # Încearcă parsing direct
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Caută blocul JSON între ```json ... ``` sau { ... }
        import re
        json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Caută primul { ... } din text
        brace_match = re.search(r"\{.*\}", text, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group(0))
            except json.JSONDecodeError:
                pass

        return None

    @abstractmethod
    def run(self, input_data: str) -> dict:
        """
        Metoda principală a agentului. Fiecare agent o implementează diferit.

        Args:
            input_data: Datele de intrare pentru agent

        Returns:
            Dict cu rezultatele procesării
        """
        pass

    def __repr__(self):
        return f"{self.name}(model={self.model}, temperature={self.temperature})"
