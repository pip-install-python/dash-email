"""
AI feature detection.

Deliberately free of heavy imports (no google.genai) so callers can ask whether
AI is available without importing the SDK or needing a key to be present.
"""
import os

from dotenv import load_dotenv

load_dotenv()


def get_api_key():
    """Return the configured Gemini key, or None when AI features are off."""
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def is_ai_enabled() -> bool:
    """True when a Gemini key is configured and AI generation can be used."""
    return bool(get_api_key())
