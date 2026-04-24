from typing import List
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

from models import Listing


def search_craigslist(query: str) -> List[Listing]:
    encoded = quote_plus(query)

    url = f"https://lasvegas.craigslist.org/search/ggg?query={encoded}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        posts = soup.find_all("li", class_="cl-static-search-result")

        for post in posts[:5]:  # limit to 5 listings
            title_tag = post.find("a", class_="cl-app-anchor")
            if not title_tag:
                continue

            title = title_tag.text.strip()
            link = title_tag["href"]

            results.append(
                Listing(
                    title=title,
                    location="Las Vegas",
                    source="Craigslist",
                    summary="Casting / gig opportunity. Tap to view details.",
                    url=link
                )
            )

        # fallback if nothing found
        if not results:
            return [
                Listing(
                    title=f"Craigslist results: {query}",
                    location="Las Vegas",
                    source="Craigslist",
                    summary="Browse local gigs and casting opportunities.",
                    url=url
                )
            ]

        return results

    except Exception as e:
        print("Craigslist error:", e)

        return [
            Listing(
                title=f"Craigslist results: {query}",
                location="Las Vegas",
                source="Craigslist",
                summary="Browse local gigs and casting opportunities.",
                url=url
            )
        ]