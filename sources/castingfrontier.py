from typing import List
from models import Listing


def search_casting_frontier(query: str) -> List[Listing]:
    """
    Casting Frontier does not expose public listings without login.
    This returns a clean, honest platform entry instead of fake listings.
    """

    return [
        Listing(
            title="Casting Frontier",
            location="Nationwide",
            source="Casting Frontier",
            summary="Create a Casting Frontier profile to access casting calls, auditions, and submissions. Login required to view opportunities.",
            url="https://castingfrontier.com/"
        )
    ]