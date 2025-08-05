# main.py

import os
from dotenv import load_dotenv

from GoogleSheets import read_sheet_as_df, update_sheet_row
from summarizer import summarize_link
from memory import parse_related_posts, get_high_performing_snippets
from generator import generate_post

def main():
    # Load environment variables
    load_dotenv()

    sheet_name = os.getenv("GOOGLE_SHEET_NAME")
    if not sheet_name:
        raise ValueError("Missing GOOGLE_SHEET_NAME in .env")

    df, sheet = read_sheet_as_df(sheet_name)

    for index, row in df.iterrows():
        if not row.get("content"):
            print(f"\n🔄 Processing row {index}...")

            topic = row.get("topic", "")
            support_link = row.get("support_links", "")
            related_posts = row.get("other_related_linkedin_posts", "")
            mapped_impressions = row.get("other_post_mapped_impressions", "")

            # Step 1: Summarize the support link
            summary = summarize_link(support_link)

            # Step 2: Memory - parse previous posts and impressions
            memory_items = parse_related_posts(related_posts, mapped_impressions)
            memory_snippets = get_high_performing_snippets(memory_items)

            # Step 3: Generate the post
            generated_post = generate_post(topic, summary, memory_snippets)

            print("✅ Generated Post:\n", generated_post)

            # Step 4: Write back to the sheet
            update_sheet_row(sheet, index, generated_post)
            print("📝 Updated content in Google Sheet.")

if __name__ == "__main__":
    main()
