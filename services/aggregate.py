from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from typing import List
from models import Listing


def aggregate_results(query: str) -> List[Listing]:
    results: List[Listing] = []

    try:
        results.extend(search_backstage(query))
    except Exception as e:
        print("Backstage error:", e)

    try:
        results.extend(search_indeed(query))
    except Exception as e:
        print("Indeed error:", e)

    try:
        results.extend(search_craigslist(query))
    except Exception as e:
        print("Craigslist error:", e)

    return results[:10]