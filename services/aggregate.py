from typing import List
from models import Listing
from sources.craigslist import search_craigslist

def aggregate_results(query: str) -> List[Listing]:
    results = []

    try:
        results.extend(search_craigslist(query))
    except Exception:
        pass

    return results[:10]
