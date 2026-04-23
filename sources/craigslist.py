from typing import List
from urllib.parse import quote_plus
from models import Listing


def search_craigslist(query: str) -> List[Listing]:
    encoded = quote_plus(query)

    return [
        Listing(
            title=f"Craigslist results for: {query}",
            location="Las Vegas",
            url=f"https://lasvegas.craigslist.org/search/sss?query={encoded}"
        )
    ]
