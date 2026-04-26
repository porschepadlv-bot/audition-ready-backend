from typing import List
from urllib.parse import quote_plus, urljoin
import requests
from bs4 import BeautifulSoup
from models import Listing


def search_entertainment_careers(query: str) -> List[Listing]:
    encoded = quote_plus(query)
    url = f"https://www.entertainmentcareers.net/jobs/s/?q={encoded}"

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

            lower_href = href.lower()

            if "/job/" not in lower_href and "/jobs/" not in lower_href:
                continue

            full_url = urljoin("https://www.entertainmentcareers.net", href)

            results.append(
                Listing(
                    title=title[:120],
                    location="Entertainment / Media",
                    source="EntertainmentCareers",
                    summary="Entertainment industry job or internship listing.",
                    url=full_url
                )
            )

            if len(results) >= 5:
                break

        if not results:
            return fallback()

        return results

    except Exception as e:
        print("Entertainment Careers error:", e)
        return fallback()


def fallback() -> List[Listing]:
    return [
        Listing(
            title="Entertainment Careers",
            location="Nationwide",
            source="EntertainmentCareers",
            summary="Browse entertainment jobs, internships, and media industry opportunities.",
            url="https://www.entertainmentcareers.net/"
        )
    ]