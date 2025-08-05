# generator.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_post_with_open_ai(topic: str, summary: str, memory_snippets: list[str]) -> tuple[str, str]:
    memory_block = "\n\n".join(memory_snippets) if memory_snippets else "None available"

    prompt = f"""
You are a technical content writer who creates engaging LinkedIn posts.

Goal: Write a short, impactful post about a software/technology topic to increase impressions and engagement.

Requirements:
- Topic: {topic}
- Based on this summary: {summary}
- Style similar to these high-impression posts: {memory_block}

Constraints:
- Max 250 words
- Use an engaging hook at the top
- Share a unique insight or technical takeaway
- End with a question or CTA to drive engagement
- Avoid hashtags or emojis

Write the post now:
"""

    print(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful and concise technical LinkedIn content writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=400
    )
    print("response:" + response)
    return response['choices'][0]['message']['content'].strip(), prompt


import os
import google.generativeai as genai


def generate_post_with_gemini(topic: str, summary: str, memory_snippets: list[str]) -> tuple[str, str]:
    # Prepare memory block
    memory_block = "\n\n".join(memory_snippets) if memory_snippets else "None available"

    # Build prompt
    prompt = f"""
You are a technical content writer who creates engaging LinkedIn posts.

Goal: Write a short, impactful post about a software/technology topic to increase impressions and engagement.

Requirements:
- Topic: {topic}
- Based on this summary: {summary}
- Style similar to these high-impression posts: {memory_block}

Constraints:
- Max 250 words
- Use an engaging hook at the top
- Share a unique insight or technical takeaway
- End with a question or CTA to drive engagement
- Avoid hashtags or emojis

Write the post now:
"""

    print("🤖 Gemini Prompt:\n", prompt)

    # Configure and call Gemini
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text.strip(), prompt
