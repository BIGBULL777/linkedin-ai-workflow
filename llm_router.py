from generator import generate_post_with_open_ai, generate_post_with_gemini
from critic import critique_post_with_open_ai, critique_post_with_gemini
import logging

PROVIDERS = ["openai", "gemini"]

def generate_content(topic: str, summary: str, memory_snippets: list[str]) -> tuple[str, str, int, str]:
    previous_feedback = ""
    previous_post = ""
    prompt = ""

    for attempt in range(5):  # Max 5 attempts to avoid infinite loops
        last_generation_error = None

        # 1. Generate post using fallback across LLMs
        for provider in PROVIDERS:
            try:
                logging.info(f"✨ Attempting post generation with {provider}...")

                if provider == "openai":
                    generated_post, prompt = generate_post_with_open_ai(topic, summary, memory_snippets, previous_feedback, previous_post)
                elif provider == "gemini":
                    generated_post, prompt = generate_post_with_gemini(topic, summary, memory_snippets, previous_feedback, previous_post)
                else:
                    continue

                logging.info(f"✅ Post generated using {provider}.")
                break

            except Exception as e:
                logging.warning(f"⚠️ {provider} generation failed: {e}")
                last_generation_error = e
                continue
        else:
            raise RuntimeError(f"All LLMs failed for generation. Last error: {last_generation_error}")

        # 2. Critique post using fallback
        last_critique_error = None
        for provider in PROVIDERS:
            try:
                logging.info(f"🔍 Critiquing post with {provider}...")

                if provider == "openai":
                    score, feedback = critique_post_with_open_ai(generated_post)
                elif provider == "gemini":
                    score, feedback = critique_post_with_gemini(generated_post)
                else:
                    continue

                logging.info(f"💬 Critique result: Score = {score}/10")

                if score >= 8:
                    return generated_post, prompt, score, feedback

                break  # Critique succeeded but score too low

            except Exception as e:
                logging.warning(f"⚠️ {provider} critique failed: {e}")
                last_critique_error = e
                continue
        else:
            raise RuntimeError(f"All LLMs failed to critique. Last error: {last_critique_error}")

        # 3. Loop again with updated feedback and previous post
        logging.info("🔁 Retrying generation with feedback...")
        previous_feedback = feedback
        previous_post = generated_post

    raise RuntimeError("❌ Failed to generate a high-quality post after multiple attempts.")
