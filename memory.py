# memory.py

import logging

def parse_related_posts(related_text: str, impressions_text: str) -> list[dict]:
    
    related = [r.strip() for r in related_text.split("||")] if related_text else []
    impressions = [int(i.strip()) for i in impressions_text.split(",") if i.strip().isdigit()] if impressions_text else []

    memory = []
    for i, post in enumerate(related):
        imp = impressions[i] if i < len(impressions) else 0
        memory.append({"text": post, "impressions": imp})

    return memory


def get_high_performing_snippets(memory: list[dict], top_n: int = 2) -> list[str]:
    sorted_posts = sorted(memory, key=lambda x: x["impressions"], reverse=True)
    top_snippets = [post["text"] for post in sorted_posts[:top_n]]
    return top_snippets
