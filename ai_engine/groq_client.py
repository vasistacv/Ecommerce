"""Groq API client wrapper for all AI features."""
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class GroqClient:
    """Wrapper around Groq API for LLM-powered features."""

    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self._client = None

    @property
    def client(self):
        if self._client is None:
            try:
                from groq import Groq
                self._client = Groq(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                raise
        return self._client

    def chat(self, messages, temperature=0.7, max_tokens=1024):
        """Send a chat completion request to Groq."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return None

    def chat_json(self, messages, temperature=0.3, max_tokens=1024):
        """Send a request and parse JSON response."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from Groq response")
            return None
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return None


# Singleton instance
groq_client = GroqClient()
