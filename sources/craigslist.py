from typing import List
from urllib.parse import quote_plus
from models import Listing
import requests
from bs4 import BeautifulSoup


def search_craigslist(query: str) -> List[Listing]:
    encoded = quote_plus(query)
    url = f"https://lasvegas.craigslist.org/search/ggg?query={encoded}"

    listings: List[Listing] = []

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        soup = BeautifulSoup(response.text, "html.parser")

        # Try modern Craigslist result cards first
        for r in soup.select(".result-row, li.cl-static-search-result, div.gallery-card"):
            title_tag = (
                r.select_one(".result-title")
                or r.select_one("a.posting-title")
                or r.select_one("a")
            )

            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = title_tag.get("href", "")

            if not title or title.lower() == "craigslist":
                continue

            if len(title) < 10:
                continue

            if link.startswith("/"):
                link = "https://lasvegas.craigslist.org" + link

            if "craigslist.org" not in link:
                continue

            listings.append(
                Listing(
                    title=title,
                    location="Las Vegas",
                    source="Craigslist",
                    summary="Casting / gig opportunity. Tap to view details.",
                    url=link
                )
            )

            if len(listings) >= 5:
                break

    except Exception as e:
        print("Craigslist scrape error:", e)

    if listings:
        return listings

    return [
        Listing(
            title=f"Craigslist gigs: {query}",
            location="Las Vegas",
            source="Craigslist",
            summary="Quick local gigs and casting posts. Tap to view results.",
            url=url
        )
    ]