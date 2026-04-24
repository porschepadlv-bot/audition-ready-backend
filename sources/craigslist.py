from typing import List
from urllib.parse import quote_plus
from models import Listing


def search_craigslist(query: str) -> List[Listing]:
    try:
        encoded = quote_plus(query)

        # ALWAYS return at least one working result
        results = [
            Listing(
                title=f"Craigslist results: {query}",
                location="Las Vegas",
                source="Craigslist",
                summary="Browse local gigs and casting opportunities on Craigslist.",
                url=f"https://lasvegas.craigslist.org/search/ggg?query={encoded}"
            )
        ]

        return results

    except Exception as e:
        print("Craigslist failure:", e)
        return []