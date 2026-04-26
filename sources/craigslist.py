from typing import List
from models import Listing
from urllib.parse import quote_plus


def search_craigslist(query: str) -> List[Listing]:
    lower_query = query.lower()
    encoded = quote_plus(query)

    city_url = "https://www.craigslist.org/search/tlg"
    location = "Multiple Cities"

    if "las vegas" in lower_query or "vegas" in lower_query:
        city_url = "https://lasvegas.craigslist.org/search/tlg"
        location = "Las Vegas"

    elif "los angeles" in lower_query or "la " in lower_query or " l.a." in lower_query:
        city_url = "https://losangeles.craigslist.org/search/tlg"
        location = "Los Angeles"

    elif "new york" in lower_query or "nyc" in lower_query:
        city_url = "https://newyork.craigslist.org/search/tlg"
        location = "New York"

    elif "atlanta" in lower_query:
        city_url = "https://atlanta.craigslist.org/search/tlg"
        location = "Atlanta"

    elif "chicago" in lower_query:
        city_url = "https://chicago.craigslist.org/search/tlg"
        location = "Chicago"

    elif "miami" in lower_query:
        city_url = "https://miami.craigslist.org/search/tlg"
        location = "Miami"

    elif "dallas" in lower_query:
        city_url = "https://dallas.craigslist.org/search/tlg"
        location = "Dallas"

    elif "houston" in lower_query:
        city_url = "https://houston.craigslist.org/search/tlg"
        location = "Houston"

    elif "seattle" in lower_query:
        city_url = "https://seattle.craigslist.org/search/tlg"
        location = "Seattle"

    elif "san francisco" in lower_query or "bay area" in lower_query:
        city_url = "https://sfbay.craigslist.org/search/tlg"
        location = "San Francisco Bay Area"

    return [
        Listing(
            title=f"Craigslist Talent Gigs: {query}",
            location=location,
            source="Craigslist",
            summary="Browse local talent, acting, modeling, and gig listings on Craigslist.",
            url=f"{city_url}?query={encoded}"
        )
    ]