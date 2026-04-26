from typing import List
from models import Listing


def search_project_casting(query: str) -> List[Listing]:
    return [
        Listing(
            title="Project Casting",
            location="Nationwide",
            source="Project Casting",
            summary="Browse casting calls, extras roles, and entertainment jobs. Account signup may be required.",
            url="https://www.projectcasting.com/"
        )
    ]