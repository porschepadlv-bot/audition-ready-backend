from typing import List
from models import Listing

def search_indeed(query: str) -> List[Listing]:
    return [
        Listing(
            title=f"Indeed Job: {query}",
            location="Las Vegas",
            source="Indeed",
            summary="Job listing from Indeed. Paid opportunity.",
            url="https://www.indeed.com/"
        )
    ]