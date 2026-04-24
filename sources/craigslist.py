from typing import List
from urllib.parse import quote_plus
from models import Listing
import requests
from bs4 import BeautifulSoup


def scrape_category(category: str, query: str) -> List[Listing]:
    encoded = quote_plus(query)
    url = f"https://lasvegas.craigslist.org/search/{category}?query={encoded}"

    results = []

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        soup = BeautifulSoup(response.text, "html.parser")

        for r in soup.select(".result-row"):
            title_tag = r.select_one(".result-title")

            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = title_tag.get("href", "")

            if not title or len(title) < 10:
                continue

            results.append(
                Listing(
                    title=title,
                    location="Las Vegas",
                    source="Craigslist",
                    summary="Casting / gig opportunity. Tap to view details.",
                    url=link
                )
            )

            if len(results) >= 3:
                break

    except Exception as e:
        print(f"Craigslist {category} error:", e)

    return results


def search_craigslist(query: str) -> List[Listing]:
    listings: List[Listing] = []

    # 🔥 search multiple categories
    listings.extend(scrape_category("ggg", query))  # gigs
    listings.extend(scrape_category("tlg", query))  # talent

    if listings:
        return listings[:5]

    encoded = quote_plus(query)
    return [
        Listing(
            title=f"Craigslist results: {query}",
            location="Las Vegas",
            source="Craigslist",
            summary="Tap to view Craigslist search results.",
            url=f"https://lasvegas.craigslist.org/search/ggg?query={encoded}"
        )
    ]