from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from typing import List
from models import Listing
from urllib.parse import quote_plus


def aggregate_results(query: str) -> List[Listing]:
    results: List[tuple] = []
    seen_urls = set()

    def add_results(new_results: List[Listing], priority: int):
        for item in new_results:
            if not item.url:
                continue

            if item.url in seen_urls:
                continue

            seen_urls.add(item.url)
            results.append((priority, item))

    # Core sources
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

    encoded = quote_plus(query)

    # FIXED sources (no more broken links)
    extra_sources = [
        (4, Listing(
            title=f"Facebook Groups: {query}",
            location="Local / Online",
            source="Facebook",
            summary="Find local casting calls in Facebook groups.",
            url=f"https://www.facebook.com/search/groups/?q={encoded}"
        )),
        (5, Listing(
            title=f"Actors Access: {query}",
            location="Nationwide",
            source="Actors Access",
            summary="Professional casting breakdowns and auditions.",
            url="https://actorsaccess.com/"
        )),
        (6, Listing(
            title=f"Playbill Jobs",
            location="Nationwide",
            source="Playbill",
            summary="Theater auditions and casting opportunities.",
            url="https://www.playbill.com/jobs"
        )),
        (7, Listing(
            title=f"Mandy Casting",
            location="Nationwide",
            source="Mandy",
            summary="Film, TV, and commercial casting jobs.",
            url="https://www.mandy.com/"
        )),
        (8, Listing(
            title=f"Casting Networks",
            location="Nationwide",
            source="Casting Networks",
            summary="Professional casting platform.",
            url="https://www.castingnetworks.com/"
        )),
        (9, Listing(
            title=f"Casting Frontier",
            location="Nationwide",
            source="Casting Frontier",
            summary="Online casting platform for actors and models.",
            url="https://www.castingfrontier.com/"
        )),
        (10, Listing(
            title=f"Entertainment Careers",
            location="Nationwide",
            source="EntertainmentCareers",
            summary="Entertainment industry jobs and internships.",
            url="https://www.entertainmentcareers.net/"
        ))
    ]

    for item in extra_sources:
        if item[1].url not in seen_urls:
            seen_urls.add(item[1].url)
            results.append(item)

    results.sort(key=lambda x: x[0])

    final_results = [item for _, item in results]

    return final_results[:10]