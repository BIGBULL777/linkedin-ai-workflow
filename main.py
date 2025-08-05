# main.py

import os
import logging
from dotenv import load_dotenv

from GoogleSheets import read_sheet_as_df, update_sheet_row
from summarizer import summarize_link
from memory import parse_related_posts, get_high_performing_snippets
from llm_router import generate_content
from logger import log_ai_thinking

MAX_TRIES = 25  # Avoid infinite loops

def main():
    load_dotenv()

    sheet_name = os.getenv("GOOGLE_SHEET_NAME")
    if not sheet_name:
        raise ValueError("Missing GOOGLE_SHEET_NAME in .env")

    df, sheet = read_sheet_as_df(sheet_name)

    for index, row in df.iterrows():
        if not row.get("content"):
            logging.info(f"🔄 Processing row {index}...")

            topic = row.get("topic", "")
            support_link = row.get("support_links", "")
            related_posts = row.get("other_related_linkedin_posts", "")
            mapped_impressions = row.get("other_post_mapped_impressions", "")

            try:
                # Step 1: Summarize
                summary = summarize_link(support_link)
                logging.info(f"📄 Summary generated for link: {support_link}")

                # Step 2: Memory
                memory_items = parse_related_posts(related_posts, mapped_impressions)
                memory_snippets = get_high_performing_snippets(memory_items)

                # Step 3: Loop until post passes critique
                final_post, final_prompt, score, feedback = "", "", 0, ""
                attempts = 0

                while score < 8 and attempts < MAX_TRIES:
                    attempts += 1
                    logging.info(f"🧠 Generating post attempt #{attempts}...")

                    # Generate post using LLM fallback
                    generated_post, prompt, score, feedback = generate_content(topic, summary, memory_snippets)
                    log_ai_thinking(index, topic, summary, memory_snippets, prompt, generated_post, score, feedback)

                    # Save if score passed
                    if score >= 8:
                        final_post = generated_post
                        final_prompt = prompt
                        logging.info(f"✅ Post accepted with score {score} on attempt #{attempts}")
                        break

                if final_post:
                    update_sheet_row(sheet, index, final_post)
                    logging.info("📝 Sheet updated for row %s", index)
                else:
                    logging.warning(f"⚠️ Failed to generate acceptable post for row {index} after {MAX_TRIES} tries.")

            except Exception as e:
                logging.error(f"❌ Error processing row {index}: {e}")

if __name__ == "__main__":
    main()
