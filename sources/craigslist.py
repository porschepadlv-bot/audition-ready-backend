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

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        seen = set()

        posts = soup.find_all("li", class_="cl-static-search-result")

        for post in posts:
            title_tag = post.find("a", class_="cl-app-anchor")
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = title_tag.get("href", "").strip()

            if not title or not link:
                continue

            if link in seen:
                continue

            seen.add(link)

            location = "Las Vegas"
            location_tag = post.find(class_="location")
            if location_tag:
                location = location_tag.get_text(strip=True)

            summary = "Casting / gig opportunity. Tap to view details."

            price_tag = post.find(class_="price")
            if price_tag:
                summary = f"{price_tag.get_text(strip=True)} · Tap to view details."

            results.append(
                Listing(
                    title=title,
                    location=location,
                    source="Craigslist",
                    summary=summary,
                    url=link
                )
            )

            if len(results) >= 5:
                break

        return results

    except Exception as e:
        print("Craigslist error:", e)
        return []