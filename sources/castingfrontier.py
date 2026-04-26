from typing import List
from models import Listing


def search_casting_frontier(query: str) -> List[Listing]:
    return [
        Listing(
            title="Casting Frontier",
            location="Nationwide",
            source="Casting Frontier",
            summary="Create a Casting Frontier profile to access auditions and casting calls. Account required.",
            url="https://castingfrontier.com/"
        )
    ]