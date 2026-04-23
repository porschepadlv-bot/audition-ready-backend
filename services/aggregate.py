from sources.backstage import search_backstage
from typing import List
from models import Listing

def aggregate_results(query: str) -> List[Listing]:
    results: List[Listing] = []

    try:
        results.extend(search_backstage(query))
    except Exception as e:
        print("Backstage error:", e)



    return results[:10]