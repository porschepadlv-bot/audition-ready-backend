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
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Craigslist bad status:", response.status_code)
            return fallback(query, url)

        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        rows = soup.find_all("li", class_="result-row")

        for row in rows[:5]:
            title_tag = row.find("a", class_="result-title")

            if not title_tag:
                continue

            title = title_tag.text.strip()
            link = title_tag.get("href")

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

        if results:
            print("Craigslist SUCCESS:", len(results))
            return results

        print("Craigslist EMPTY — using fallback")
        return fallback(query, url)

    except Exception as e:
        print("Craigslist ERROR:", e)
        return fallback(query, f"https://lasvegas.craigslist.org/search/ggg?query={quote_plus(query)}")


def fallback(query: str, url: str) -> List[Listing]:
    return [
        Listing(
            title=f"Craigslist results: {query}",
            location="Las Vegas",
            source="Craigslist",
            summary="Browse local gigs and casting opportunities.",
            url=url
        )
    ]