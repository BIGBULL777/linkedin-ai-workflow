import logging

from generator import generate_post_with_open_ai, generate_post_with_gemini

PROVIDERS = ["openai", "gemini"]


def generate_content(prompt: str, summary, snippets):
    last_error = None
    for provider in PROVIDERS:
        try:
            logging.info(f"Trying LLM: {provider}")
            if provider == "openai":
                return generate_post_with_open_ai(prompt, summary, snippets)
            elif provider == "gemini":
                return generate_post_with_gemini(prompt, summary, snippets)
        except Exception as e:
            logging.warning(f"⚠️ {provider} failed: {e}")
            last_error = e
    raise RuntimeError(f"All LLMs failed. Last error: {last_error}")
