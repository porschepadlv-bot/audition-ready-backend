from typing import List
from models import Listing
import requests
from bs4 import BeautifulSoup


def search_craigslist(query: str) -> List[Listing]:
    listings: List[Listing] = []

    url = f"https://lasvegas.craigslist.org/search/ggg?query={query}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.select(".result-row")

    for r in results[:5]:  # limit to 5 results
        title_tag = r.select_one(".result-title")
        location_tag = r.select_one(".result-hood")

        title = title_tag.text if title_tag else "No title"
        link = title_tag["href"] if title_tag else ""
        location = location_tag.text if location_tag else "Las Vegas"

        listings.append(
            Listing(
                title=title,
                location=location,
                source="Craigslist",
                summary="Casting / gig opportunity",
                url=link,
            )
        )

    return listings