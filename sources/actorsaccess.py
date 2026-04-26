from typing import List
import requests
from bs4 import BeautifulSoup
from models import Listing


def search_actors_access(query: str) -> List[Listing]:
    url = "https://actorsaccess.com/projects/?view=breakdowns"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text("\n", strip=True)

        blocks = text.split("TITLE:")

        first_title = ""

        for block in blocks[1:6]:
            lines = [line.strip() for line in block.split("\n") if line.strip()]

            if lines:
                first_title = lines[0]
                break

        summary = "Browse current casting breakdowns on Actors Access."

        if first_title:
            summary = f"Includes listings like “{first_title}” and more casting breakdowns."

        return [
            Listing(
                title="Actors Access",
                location="Nationwide",
                source="Actors Access",
                summary=summary,
                url="https://actorsaccess.com/projects/?view=breakdowns"
            )
        ]

    except Exception as e:
        print("Actors Access error:", e)
        return []