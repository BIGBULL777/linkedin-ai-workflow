# logger.py
import logging
from pathlib import Path

# Setup
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

def log_ai_thinking(row_index: int, topic: str, summary: str, memory: list[str], prompt: str, output: str, score,
                    feedback):
    ai_log_path = LOG_DIR / f"row_{row_index}_ai_thinking.txt"
    with open(ai_log_path, "w") as f:
        f.write(f"🧠 Topic: {topic}\n\n")
        f.write("📄 Summary:\n" + summary + "\n\n")
        f.write("🧠 Memory Snippets:\n" + "\n---\n".join(memory) + "\n\n")
        f.write("💬 Prompt Sent to GPT:\n" + prompt + "\n\n")
        f.write("📝 Output:\n" + output + "\n")
        if score is not None:
            print(f"\n🔍 Critique Score: {score}/10")
    if feedback:
        print(f"🗒️ Critique Feedback:\n{feedback}")
    print("=" * 60 + "\n")


import logging

logging.basicConfig(
    filename="post_generation.log",
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)

def log_post_generation(llm: str, topic: str, prompt: str, content: str, round_num: int, score: int = None, feedback: str = None):
    log_entry = f"""
[🔁 Round {round_num}] ✨ Post generated using {llm}
Topic: {topic}
---------------------
Prompt:
{prompt}
---------------------
Generated Post:
{content}
---------------------
Score: {score if score is not None else 'N/A'}
Feedback: {feedback if feedback else 'N/A'}
---------------------
"""
    logging.info(log_entry)
