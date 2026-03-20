import feedparser
import datetime
from sources import SOURCES

def fetch_articles(max_per_source=10, days_back=1):
    """Fetch recent articles from all RSS sources."""
    all_articles = []
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_back)

    for source in SOURCES:
        try:
            feed = feedparser.parse(source["rss"])
            count = 0
            for entry in feed.entries:
                if count >= max_per_source:
                    break

                # Parse published date if available
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime.datetime(*entry.published_parsed[:6],
                                                  tzinfo=datetime.timezone.utc)

                # Skip if older than cutoff (only if date available)
                if published and published < cutoff:
                    continue

                article = {
                    "source_name": source["name"],
                    "source_bias": source["bias"],
                    "title": entry.get("title", "").strip(),
                    "summary": entry.get("summary", entry.get("description", ""))[:500].strip(),
                    "link": entry.get("link", ""),
                    "published": published.isoformat() if published else "unknown",
                }

                # Skip articles with no meaningful content
                if article["title"] and (article["summary"] or article["link"]):
                    all_articles.append(article)
                    count += 1

            print(f"  ✓ {source['name']}: {count} articles")

        except Exception as e:
            print(f"  ✗ {source['name']}: failed ({e})")

    print(f"\nTotal articles fetched: {len(all_articles)}")
    return all_articles
