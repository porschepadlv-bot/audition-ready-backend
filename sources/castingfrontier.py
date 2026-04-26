from typing import List
import requests
from bs4 import BeautifulSoup
from models import Listing


def search_casting_frontier(query: str) -> List[Listing]:
    url = "https://castingfrontier.com/auditions"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    results: List[Listing] = []

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return fallback()

        soup = BeautifulSoup(response.text, "html.parser")

        # Try grabbing visible text blocks (site is JS heavy)
        cards = soup.find_all("div")

        for card in cards:
            text = card.get_text(strip=True)

            if len(text) < 20:
                continue

            # basic filter to catch casting-like entries
            keywords = ["role", "casting", "actor", "model", "film", "project"]

            if not any(k in text.lower() for k in keywords):
                continue

            title = text[:80]

            results.append(
                Listing(
                    title=title,
                    location="Nationwide",
                    source="Casting Frontier",
                    summary="Casting opportunity from Casting Frontier.",
                    url="https://castingfrontier.com/auditions"
                )
            )

            if len(results) >= 5:
                break

        # If scraping fails → fallback
        if not results:
            return fallback()

        return results

    except Exception as e:
        print("Casting Frontier error:", e)
        return fallback()


def fallback() -> List[Listing]:
    return [
        Listing(
            title="Casting Frontier",
            location="Nationwide",
            source="Casting Frontier",
            summary="Browse casting opportunities on Casting Frontier. Account may be required.",
            url="https://castingfrontier.com/auditions"
        )
    ]