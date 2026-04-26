from typing import List
from models import Listing


def search_craigslist(query: str) -> List[Listing]:
    return [
        Listing(
            title="Craigslist Talent Gigs",
            location="Choose Your City",
            source="Craigslist",
            summary="Open Craigslist talent gigs and choose your city to browse local acting, modeling, and talent opportunities.",
            url="https://www.craigslist.org/about/sites"
        )
    ]