# generator.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_post_with_open_ai(
        topic: str,
        summary: str,
        memory_snippets: list[str],
        previous_feedback: str = "",
        previous_post: str = ""
) -> tuple[str, str]:
    memory_block = "\n\n".join(memory_snippets) if memory_snippets else "None available"

    # Build the dynamic prompt
    prompt = f"""
You are a technical content writer who creates high-performing LinkedIn posts.

Goal:
Write a short, engaging, insightful post about the following topic to maximize impressions and engagement.

🧠 Topic: {topic}

📚 Based on this summary:
{summary}

📈 Style should reflect these top-performing posts:
{memory_block}

{f"🔁 Previous attempt:{previous_post}" if previous_post else ""}
{f"🧐 Feedback from critique:{previous_feedback}" if previous_feedback else ""}

✍️ Constraints:
- No word limit
- Start with an engaging hook
- Include a unique insight or technical takeaway
- End with a question or CTA to drive interaction
- No hashtags or emojis

Now write the improved LinkedIn post:
"""

    print("🧾 Prompt Sent to OpenAI:\n", prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a concise and engaging technical LinkedIn content writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )

    content = response['choices'][0]['message']['content'].strip()
    return content, prompt
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_post_with_gemini(
        topic: str,
        summary: str,
        memory_snippets: list[str],
        previous_feedback: str = "",
        previous_post: str = ""
) -> tuple[str, str]:
    memory_block = "\n\n".join(memory_snippets) if memory_snippets else "None available"

    prompt = f"""
You are a technical content writer who creates high-performing LinkedIn posts.

Goal:
Write a short, engaging, insightful post about the following topic to maximize impressions and engagement.

🧠 Topic: {topic}

📚 Based on this summary:
{summary}

📈 Style should reflect these top-performing posts:
{memory_block}

{f"🔁 Previous attempt:{previous_post}" if previous_post else ""}
{f"🧐 Feedback from critique:{previous_feedback}" if previous_feedback else ""}

✍️ Constraints:
- No word limit
- Start with an engaging hook
- Include a unique insight or technical takeaway
- End with a question or CTA to drive interaction
- No hashtags or emojis

Now write the improved LinkedIn post:
"""

    print("🧾 Prompt Sent to Gemini:\n", prompt)

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        content = response.text.strip()
        return content, prompt
    except Exception as e:
        raise RuntimeError(f"Gemini generation failed: {e}")
