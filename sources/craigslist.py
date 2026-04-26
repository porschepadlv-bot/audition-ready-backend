from typing import List
from models import Listing


def search_craigslist(query: str) -> List[Listing]:

    # Default to major acting cities (no broken URLs)
    sources = [
        ("Los Angeles", "https://losangeles.craigslist.org/search/tlg"),
        ("New York", "https://newyork.craigslist.org/search/tlg"),
        ("Atlanta", "https://atlanta.craigslist.org/search/tlg"),
        ("Las Vegas", "https://lasvegas.craigslist.org/search/tlg"),
    ]

    listings: List[Listing] = []

    for city, url in sources:
        listings.append(
            Listing(
                title=f"Craigslist Talent Gigs ({city})",
                location=city,
                source="Craigslist",
                summary="Browse acting, modeling, and talent gigs.",
                url=url
            )
        )

    return listings