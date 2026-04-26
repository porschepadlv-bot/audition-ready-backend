from typing import List
from models import Listing


def search_mandy(query: str) -> List[Listing]:
    return [
        Listing(
            title="Mandy",
            location="Nationwide",
            source="Mandy",
            summary="Browse casting calls and production jobs on Mandy. Account signup may be required.",
            url="https://www.mandy.com/"
        )
    ]