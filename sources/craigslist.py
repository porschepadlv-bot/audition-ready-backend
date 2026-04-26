from typing import List
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

from models import Listing


def simplify_query(query: str) -> str:
    clean = query.lower()

    keywords = []

    if "acting" in clean or "actor" in clean:
        keywords.append("acting")

    if "model" in clean or "modeling" in clean:
        keywords.append("model")

    if "casting" in clean or "audition" in clean:
        keywords.append("casting")

    if "film" in clean or "movie" in clean:
        keywords.append("film")

    if "commercial" in clean:
        keywords.append("commercial")

    if not keywords:
        words_to_remove = {
            "jobs", "job", "in", "near", "me", "las", "vegas",
            "los", "angeles", "new", "york", "seattle",
            "casting", "auditions", "audition"
        }

        words = [
            word for word in clean.split()
            if word not in words_to_remove
        ]

        if words:
            keywords.append(words[0])
        else:
            keywords.append("casting")

    return " ".join(dict.fromkeys(keywords))


def search_craigslist(query: str) -> List[Listing]:
    clean_query = simplify_query(query)
    encoded = quote_plus(clean_query)

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