from typing import List
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
from models import Listing


def search_craigslist(query: str) -> List[Listing]:
    try:
        encoded = quote_plus(query)
        url = f"https://lasvegas.craigslist.org/search/ggg?query={encoded}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        listings = soup.select(".result-row")[:5]  # limit to 5 results

        for item in listings:
            title_tag = item.select_one(".result-title")
            link = title_tag["href"] if title_tag else None
            title = title_tag.text.strip() if title_tag else "Craigslist listing"

            if link:
                results.append(
                    Listing(
                        title=title,
                        location="Las Vegas",
                        source="Craigslist",
                        summary="Casting / gig opportunity from Craigslist.",
                        url=link
                    )
                )

        # fallback if nothing found
        if not results:
            results.append(
                Listing(
                    title=f"Craigslist results: {query}",
                    location="Las Vegas",
                    source="Craigslist",
                    summary="Browse local gigs on Craigslist.",
                    url=url
                )
            )

        return results

    except Exception as e:
        print("Craigslist scraper error:", e)
        return []