from typing import List
from models import Listing


def search_indeed(query: str) -> List[Listing]:
    return [
        Listing(
            title=f"Indeed jobs: {query}",
            location="Las Vegas",
            source="Indeed",
            summary="Tap to view matching Indeed job results.",
            url="https://www.indeed.com/jobs?q=" + query.replace(" ", "+")
        )
    ]