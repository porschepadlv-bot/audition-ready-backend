from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from typing import List
from models import Listing


def aggregate_results(query: str) -> List[Listing]:
    results: List[Listing] = []
    seen_urls = set()

    def add_results(new_results: List[Listing], priority: int):
        for item in new_results:
            if not item.url:
                continue

            if item.url in seen_urls:
                continue

            seen_urls.add(item.url)

            # Attach priority score
            item.priority = priority
            results.append(item)

    try:
        add_results(search_backstage(query), priority=1)  # BEST
    except Exception as e:
        print("Backstage error:", e)

    try:
        add_results(search_indeed(query), priority=2)
    except Exception as e:
        print("Indeed error:", e)

    try:
        add_results(search_craigslist(query), priority=3)
    except Exception as e:
        print("Craigslist error:", e)

    # Sort by priority (lower = better)
    results.sort(key=lambda x: getattr(x, "priority", 99))

    return results[:10]