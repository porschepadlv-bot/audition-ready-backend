from typing import List
from models import Listing


def search_casting_networks(query: str) -> List[Listing]:
    return [
        Listing(
            title="Casting Networks",
            location="Nationwide",
            source="Casting Networks",
            summary="Browse casting opportunities on Casting Networks. Account signup may be required.",
            url="https://www.castingnetworks.com/"
        )
    ]