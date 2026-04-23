from typing import List
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
from models import Listing


def search_craigslist(query: str) -> List[Listing]:
    listings: List[Listing] = []

    encoded = quote_plus(query)
    url = f"https://lasvegas.craigslist.org/search/ggg?query={encoded}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        results = soup.select(".result-row")

        for r in results[:10]:
            title_tag = r.select_one(".result-title")
            location_tag = r.select_one(".result-hood")

            title = title_tag.text if title_tag else "No title"
            link = title_tag["href"] if title_tag else url
            location = location_tag.text.strip("()") if location_tag else "Las Vegas"

            listings.append(
                Listing(
                    title=title,
                    location=location,
                    source="Craigslist",
                    summary="Casting / gig opportunity",
                    url=link
                )
            )

    except Exception as e:
        print("Craigslist scraping error:", e)

    return listings