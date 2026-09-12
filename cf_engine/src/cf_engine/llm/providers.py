import os
import json
import requests
from typing import Optional
from .base import LLMProvider
from .schemas import SemanticSignals
from .prompts import SEMANTIC_INTERPRETATION_PROMPT

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-3.5-flash"):
        self.api_key = api_key or os.environ.get("CF_LLM_API_KEY")
        self.model = model
        self.timeout = int(os.environ.get("CF_LLM_TIMEOUT_SECONDS", "20"))
        
    def interpret_response(
        self,
        conversation_context: dict,
        seller_response: str,
        objective_signals: dict,
    ) -> SemanticSignals:
        if not self.api_key:
            raise ValueError("No API key provided")
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        prompt_data = {
            "conversation_context": conversation_context,
            "seller_response": seller_response,
            "objective_signals": objective_signals
        }
        
        # We need a proper JSON schema representation for Gemini's structured output.
        # But for simplicity, we can just ask for JSON matching the schema and parse it.
        # It's highly reliable with modern models.
        
        schema = SemanticSignals.model_json_schema()
        
        payload = {
            "system_instruction": {
                "parts": [{"text": SEMANTIC_INTERPRETATION_PROMPT + "\\n\\nHere is the schema:\\n" + json.dumps(schema)}]
            },
            "contents": [
                {
                    "parts": [{"text": json.dumps(prompt_data, indent=2)}]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
            }
        }
        
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=self.timeout)
        response.raise_for_status()
        
        data = response.json()
        
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            # It might have markdown block
            if text.startswith("```json"):
                text = text.split("```json")[1].rsplit("```", 1)[0].strip()
            elif text.startswith("```"):
                text = text.split("```")[1].rsplit("```", 1)[0].strip()
            
            parsed = json.loads(text)
            
            # Ensure numbers are clamped and types are good
            return SemanticSignals(**parsed)
            
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {e}")

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("CF_LLM_API_KEY")
        self.model = model
        self.timeout = int(os.environ.get("CF_LLM_TIMEOUT_SECONDS", "20"))
        
    def interpret_response(
        self,
        conversation_context: dict,
        seller_response: str,
        objective_signals: dict,
    ) -> SemanticSignals:
        if not self.api_key:
            raise ValueError("No API key provided")
            
        url = "https://api.openai.com/v1/chat/completions"
        
        prompt_data = {
            "conversation_context": conversation_context,
            "seller_response": seller_response,
            "objective_signals": objective_signals
        }
        
        schema = SemanticSignals.model_json_schema()
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SEMANTIC_INTERPRETATION_PROMPT + "\\n\\nHere is the schema:\\n" + json.dumps(schema)},
                {"role": "user", "content": json.dumps(prompt_data, indent=2)}
            ],
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(
            url, 
            json=payload, 
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}, 
            timeout=self.timeout
        )
        response.raise_for_status()
        
        data = response.json()
        
        try:
            text = data["choices"][0]["message"]["content"]
            parsed = json.loads(text)
            return SemanticSignals(**parsed)
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {e}")
