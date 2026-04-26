from typing import List
from models import Listing


def search_craigslist(query: str) -> List[Listing]:
    return [
        Listing(
            title="Craigslist Talent Gigs",
            location="Las Vegas",
            source="Craigslist",
            summary="Browse local talent, acting, modeling, and gig listings.",
            url="https://lasvegas.craigslist.org/search/tlg#search=2~thumb~0"
        )
    ]