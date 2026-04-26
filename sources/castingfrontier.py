from typing import List
from models import Listing


def search_casting_frontier(query: str) -> List[Listing]:
    return [
        Listing(
            title="Casting Frontier",
            location="Nationwide",
            source="Casting Frontier",
            summary="Browse casting opportunities on Casting Frontier. Account signup may be required.",
            url="https://castingfrontier.com/"
        )
    ]