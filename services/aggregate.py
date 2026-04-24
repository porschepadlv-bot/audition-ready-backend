from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from typing import List
from models import Listing
from urllib.parse import quote_plus


def aggregate_results(query: str) -> List[Listing]:
    results: List[tuple] = []  # (priority, Listing)
    seen_urls = set()

    def add_results(new_results: List[Listing], priority: int):
        for item in new_results:
            if not item.url:
                continue

            if item.url in seen_urls:
                continue

            seen_urls.add(item.url)
            results.append((priority, item))

    # Existing sources
    try:
        add_results(search_backstage(query), priority=1)
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

    # 🔥 NEW SOURCES (STABLE LINKS)
    encoded = quote_plus(query)

    extra_sources = [
        (
            4,
            Listing(
                title=f"Casting Networks: {query}",
                location="Nationwide",
                source="Casting Networks",
                summary="Browse professional casting calls.",
                url=f"https://www.castingnetworks.com/search/?q={encoded}"
            )
        ),
        (
            5,
            Listing(
                title=f"Mandy Casting: {query}",
                location="Nationwide",
                source="Mandy",
                summary="Film, TV, and commercial casting calls.",
                url=f"https://www.mandy.com/jobs?search={encoded}"
            )
        ),
        (
            6,
            Listing(
                title=f"Facebook Groups: {query}",
                location="Local / Online",
                source="Facebook",
                summary="Find local casting calls in Facebook groups.",
                url=f"https://www.facebook.com/search/groups/?q={encoded}"
            )
        )
    ]

    for item in extra_sources:
        if item[1].url not in seen_urls:
            seen_urls.add(item[1].url)
            results.append(item)

    # Sort by priority
    results.sort(key=lambda x: x[0])

    final_results = [item for _, item in results]

    return final_results[:10]