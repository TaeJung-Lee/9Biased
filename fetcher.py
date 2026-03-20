import requests
import os
from dotenv import load_dotenv
from sources import SOURCES

load_dotenv()

# Map source names to NewsAPI domain names
SOURCE_DOMAIN_MAP = {
    "Reuters": "reuters.com",
    "Associated Press": "apnews.com",
    "The Hill": "thehill.com",
    "Fortune": "fortune.com",
    "The Atlantic": "theatlantic.com",
    "Mother Jones": "motherjones.com",
    "Breitbart": "breitbart.com",
    "Newsmax": "newsmax.com",
    "Daily Mail": "dailymail.co.uk",
    "Jacobin": "jacobinmag.com",
}

# Bias lookup by source name
BIAS_MAP = {s["name"]: s["bias"] for s in SOURCES}


def fetch_articles(max_per_source=5, days_back=1):
    """Fetch recent articles using NewsAPI."""
    api_key = os.environ.get("NEWS_API_KEY", "")
    if not api_key:
        print("  ✗ NEWS_API_KEY not set in .env")
        return []

    all_articles = []

    # Fetch top headlines from NewsAPI
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "language": "en",
        "country": "us",
        "pageSize": 100,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        print(f"  NewsAPI returned {len(articles)} articles")

        for article in articles:
            source_name = article.get("source", {}).get("name", "Unknown")
            title = (article.get("title") or "").strip()
            description = (article.get("description") or "").strip()
            url_link = article.get("url", "")

            if not title or title == "[Removed]":
                continue

            # Try to match to a known source bias
            bias = "center"
            for known_name, known_bias in BIAS_MAP.items():
                if known_name.lower() in source_name.lower():
                    bias = known_bias
                    break

            all_articles.append({
                "source_name": source_name,
                "source_bias": bias,
                "title": title,
                "summary": description[:500] if description else title,
                "link": url_link,
                "published": article.get("publishedAt", "unknown"),
            })

    except Exception as e:
        print(f"  ✗ NewsAPI fetch failed: {e}")

    # Also fetch everything category for more variety
    try:
        params2 = {
            "apiKey": api_key,
            "language": "en",
            "country": "us",
            "category": "politics",
            "pageSize": 50,
        }
        response2 = requests.get(url, params=params2, timeout=10)
        data2 = response2.json()
        for article in data2.get("articles", []):
            title = (article.get("title") or "").strip()
            if not title or title == "[Removed]":
                continue
            source_name = article.get("source", {}).get("name", "Unknown")
            bias = "center"
            for known_name, known_bias in BIAS_MAP.items():
                if known_name.lower() in source_name.lower():
                    bias = known_bias
                    break
            all_articles.append({
                "source_name": source_name,
                "source_bias": bias,
                "title": title,
                "summary": (article.get("description") or title)[:500],
                "link": article.get("url", ""),
                "published": article.get("publishedAt", "unknown"),
            })
    except Exception as e:
        print(f"  ✗ Politics category fetch failed: {e}")

    # Deduplicate by title
    seen = set()
    unique = []
    for a in all_articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)

    print(f"\nTotal articles fetched: {len(unique)}")
    return unique
