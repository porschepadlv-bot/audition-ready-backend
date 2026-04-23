from typing import List
from models import Listing


def search_backstage(query: str) -> List[Listing]:
    # TEMP mock (we'll replace with real scraping/API later)

    return [
        Listing(
            title=f"Backstage Casting: {query}",
            location="Las Vegas",
            source="Backstage",
            summary="Casting call for actors/models. Paid opportunity.",
            url="https://www.backstage.com/"
        )
    ]