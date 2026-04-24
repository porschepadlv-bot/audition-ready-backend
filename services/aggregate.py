from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from typing import List
from models import Listing


def aggregate_results(query: str) -> List[Listing]:
    results: List[Listing] = []
    seen_urls = set()

    def add_results(new_results: List[Listing]):
        for item in new_results:
            if item.url not in seen_urls:
                seen_urls.add(item.url)
                results.append(item)

    # Backstage
    try:
        add_results(search_backstage(query))
    except Exception as e:
        print("Backstage error:", e)

    # Indeed
    try:
        add_results(search_indeed(query))
    except Exception as e:
        print("Indeed error:", e)

    # Craigslist (RESTORED)
    try:
        add_results(search_craigslist(query))
    except Exception as e:
        print("Craigslist error:", e)

    return results[:10]