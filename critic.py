import openai

def critique_post_with_open_ai(post: str) -> tuple[int, str]:
    critique_prompt = f"""
You are a LinkedIn content strategist.

Critique this post and rate it on a scale of 1 to 10 based on:

1. Viewer eagerness to read
2. Is it too vague?
3. Is it too advanced?
4. Can it be explained to a 6-year-old?
5. Strength of the hook line
6. Potential to maximize impressions

Post:
\"\"\"
{post}
\"\"\"

Reply in this format:
Score: X/10
Feedback: <short explanation>
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a blunt, helpful LinkedIn strategist."},
            {"role": "user", "content": critique_prompt}
        ],
        temperature=0,
        max_tokens=300
    )

    content = response['choices'][0]['message']['content']
    try:
        score_line = [line for line in content.splitlines() if "Score:" in line][0]
        score = int(score_line.split(":")[1].strip().replace("/10", "").strip())
    except Exception:
        score = 0

    feedback = content
    return score, feedback



import google.generativeai as genai
import logging

def critique_post_with_gemini(post: str) -> tuple[int, str]:
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
You're a LinkedIn content critique assistant.

Evaluate the following post based on:
1. Viewer eagerness while reading
2. Whether it's too vague
3. Whether it's too advanced
4. Can it be explained to a 6-year-old?
5. Hook line quality
6. Potential to maximize impressions

Instructions:
- Score the post from 1 to 10
- Provide 1–2 lines of feedback on what could improve
- Be strict. Only give 8+ if it's truly strong.

Post:
\"\"\"
{post}
\"\"\"

Respond in this format:
Score: <number>/10
Feedback: <brief explanation>
"""

    response = model.generate_content(prompt)
    output = response.text.strip()
    logging.info(f"🔍 Critique Output (Gemini):\n{output}")

    # Parse score
    try:
        score_line = [line for line in output.splitlines() if "score" in line.lower()][0]
        score = int("".join(filter(str.isdigit, score_line.split("/")[0])))
    except Exception as e:
        logging.warning(f"⚠️ Failed to extract score from Gemini response: {e}")
        score = 0

    return score, output

