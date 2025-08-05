# summarizer.py

from newspaper import Article
import logging

logging.basicConfig(level=logging.INFO)

def summarize_link(link: str) -> str:
    try:
        article = Article(link)
        article.download()
        article.parse()
        article.nlp()  # Performs summary, keywords, etc.
        summary = article.summary

        logging.info(f"✅ Summarized: {link}")
        return summary or article.text[:500]

    except Exception as e:
        logging.warning(f"⚠️ Failed to summarize {link}: {e}")
        return ""
