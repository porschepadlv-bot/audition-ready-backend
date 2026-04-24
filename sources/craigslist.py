from typing import List
from urllib.parse import quote_plus
from models import Listing


def search_craigslist(query: str) -> List[Listing]:
    encoded = quote_plus(query)

    return [
        Listing(
            title=f"Craigslist quick gigs: {query}",
            location="Las Vegas",
            source="Craigslist",
            summary="Quick local gigs and casting posts. Tap to view matching Craigslist results.",
            url=f"https://lasvegas.craigslist.org/search/ggg?query={encoded}"
        )
    ]