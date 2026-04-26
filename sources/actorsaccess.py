from typing import List
import requests
from bs4 import BeautifulSoup
from models import Listing


def search_actors_access(query: str) -> List[Listing]:
    url = "https://actorsaccess.com/projects/?view=breakdowns"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    results: List[Listing] = []

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text("\n", strip=True)

        # Split into listing blocks
        blocks = text.split("TITLE:")

        for block in blocks[1:6]:  # grab up to 5 listings
            lines = [line.strip() for line in block.split("\n") if line.strip()]

            if not lines:
                continue

            title = lines[0]

            results.append(
                Listing(
                    title=title,
                    location="Nationwide",
                    source="Actors Access",
                    summary="Casting breakdown from Actors Access.",
                    url="https://actorsaccess.com/projects/?view=breakdowns"
                )
            )

        return results

    except Exception as e:
        print("Actors Access error:", e)
        return []