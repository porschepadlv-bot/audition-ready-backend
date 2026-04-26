from typing import List
from urllib.parse import quote_plus
from models import Listing


def search_indeed(query: str) -> List[Listing]:
    encoded = quote_plus(query)

    return [
        Listing(
            title=f"Indeed jobs: {query}",
            location="Nationwide",
            source="Indeed",
            summary="Browse matching job results on Indeed. Sign up may be required.",
            url=f"https://www.indeed.com/jobs?q={encoded}"
        )
    ]