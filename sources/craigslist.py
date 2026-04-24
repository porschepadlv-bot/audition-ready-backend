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

        for a in soup.select("a")[:50]:
            title = a.get_text(strip=True)
            link = a.get("href", "")

            # 🚫 skip junk titles
            if not title or title.lower() in ["craigslist"]:
                continue

            # 🚫 skip very short / useless titles
            if len(title) < 10:
                continue

            # 🚫 skip bad links
            if "craigslist.org" not in link and not link.startswith("/"):
                continue

            # fix relative links
            if link.startswith("/"):
                link = "https://lasvegas.craigslist.org" + link

            listings.append(
                Listing(
                    title=title,
                    location="Las Vegas",
                    source="Craigslist",
                    summary="Casting / gig opportunity. Tap to view details.",
                    url=link
                )
            )

            # limit results
            if len(listings) >= 5:
                break

    except Exception as e:
        print("Craigslist scrape error:", e)

    # fallback if nothing found
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