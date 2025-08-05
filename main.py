# main.py

import os
from dotenv import load_dotenv
import logging

from GoogleSheets import read_sheet_as_df, update_sheet_row
from summarizer import summarize_link
from memory import parse_related_posts, get_high_performing_snippets
from generator import generate_post
from logger import log_ai_thinking

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

                # Step 3: Generate Post
                generated_post, prompt = generate_post(topic, summary, memory_snippets)
                logging.info(f"✅ Post generated for topic: {topic}")

                # Step 4: Save thinking
                log_ai_thinking(index, topic, summary, memory_snippets, prompt, generated_post)

                # Step 5: Update sheet
                update_sheet_row(sheet, index, generated_post)
                logging.info("📝 Sheet updated for row %s", index)

            except Exception as e:
                logging.error(f"❌ Error processing row {index}: {e}")

if __name__ == "__main__":
    main()
