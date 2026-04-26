from typing import List
from models import Listing
from urllib.parse import quote_plus


def search_craigslist(query: str) -> List[Listing]:
    encoded = quote_plus(query)

    return [
        Listing(
            title=f"Craigslist Talent Gigs: {query}",
            location="Local",
            source="Craigslist",
            summary="Browse local acting, modeling, and talent gigs. Results vary by city and posting quality.",
            url=f"https://www.craigslist.org/search/tlg?query={encoded}"
        )
    ]