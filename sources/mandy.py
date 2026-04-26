from typing import List
from urllib.parse import quote_plus, urljoin
import requests
from bs4 import BeautifulSoup
from models import Listing


def search_mandy(query: str) -> List[Listing]:
    encoded = quote_plus(query)
    url = f"https://www.mandy.com/jobs?q={encoded}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return fallback()

        soup = BeautifulSoup(response.text, "html.parser")
        results: List[Listing] = []

        links = soup.find_all("a", href=True)

        for link in links:
            title = link.get_text(" ", strip=True)
            href = link.get("href", "")

            if not title or len(title) < 8:
                continue

            lower_title = title.lower()
            lower_href = href.lower()

            keywords = [
                "actor", "acting", "model", "casting",
                "film", "tv", "theatre", "theater",
                "commercial", "role"
            ]

            if not any(word in lower_title for word in keywords):
                continue

            if "job" not in lower_href and "casting" not in lower_href:
                continue

            full_url = urljoin("https://www.mandy.com", href)

            results.append(
                Listing(
                    title=title[:120],
                    location="Nationwide",
                    source="Mandy",
                    summary="Casting or production opportunity from Mandy.",
                    url=full_url
                )
            )

            if len(results) >= 5:
                break

        if not results:
            return fallback()

        return results

    except Exception as e:
        print("Mandy error:", e)
        return fallback()


def fallback() -> List[Listing]:
    return [
        Listing(
            title="Mandy",
            location="Nationwide",
            source="Mandy",
            summary="Browse casting jobs in film, TV, theatre, and commercials. Account signup may be required.",
            url="https://www.mandy.com/jobs"
        )
    ]