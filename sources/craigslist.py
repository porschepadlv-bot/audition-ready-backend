from typing import List
from models import Listing


def search_craigslist(query: str) -> List[Listing]:
    return [
        Listing(
            title="Craigslist Talent Gigs - Los Angeles",
            location="Los Angeles",
            source="Craigslist",
            summary="Browse local acting, modeling, and talent gigs in Los Angeles.",
            url="https://losangeles.craigslist.org/search/tlg"
        ),
        Listing(
            title="Craigslist Talent Gigs - New York",
            location="New York",
            source="Craigslist",
            summary="Browse local acting, modeling, and talent gigs in New York.",
            url="https://newyork.craigslist.org/search/tlg"
        ),
        Listing(
            title="Craigslist Talent Gigs - Atlanta",
            location="Atlanta",
            source="Craigslist",
            summary="Browse local acting, modeling, and talent gigs in Atlanta.",
            url="https://atlanta.craigslist.org/search/tlg"
        ),
        Listing(
            title="Craigslist Talent Gigs - Las Vegas",
            location="Las Vegas",
            source="Craigslist",
            summary="Browse local acting, modeling, and talent gigs in Las Vegas.",
            url="https://lasvegas.craigslist.org/search/tlg"
        )
    ]