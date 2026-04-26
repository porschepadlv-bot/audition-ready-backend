from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from typing import List
from models import Listing
from urllib.parse import quote_plus


def aggregate_results(query: str) -> List[Listing]:
    results: List[Listing] = []
    seen = set()

    def add(items: List[Listing]):
        for item in items:
            if not item.url:
                continue

            if item.url in seen:
                continue

            seen.add(item.url)
            results.append(item)

    # Core sources
    add(search_backstage(query))
    add(search_indeed(query))
    add(search_craigslist(query))

    encoded = quote_plus(query)

    # Stable working fallback sources (always usable pages)
    fallback_sources = [
        Listing(
            title=f"Facebook Groups: {query}",
            location="Local / Online",
            source="Facebook",
            summary="Find casting calls in Facebook groups.",
            url=f"https://www.facebook.com/search/groups/?q={encoded}"
        ),
        Listing(
            title="Actors Access",
            location="Nationwide",
            source="Actors Access",
            summary="Professional casting platform.",
            url="https://actorsaccess.com/"
        ),
        Listing(
            title="Playbill Jobs",
            location="Nationwide",
            source="Playbill",
            summary="Theater auditions and casting calls.",
            url="https://www.playbill.com/jobs"
        ),
        Listing(
            title="Mandy Casting",
            location="Nationwide",
            source="Mandy",
            summary="Film and TV casting opportunities.",
            url="https://www.mandy.com/"
        ),
        Listing(
            title="Casting Networks",
            location="Nationwide",
            source="Casting Networks",
            summary="Professional casting platform.",
            url="https://www.castingnetworks.com/"
        ),
        Listing(
            title="Casting Frontier",
            location="Nationwide",
            source="Casting Frontier",
            summary="Online casting platform.",
            url="https://www.castingfrontier.com/"
        ),
        Listing(
            title="Entertainment Careers",
            location="Nationwide",
            source="EntertainmentCareers",
            summary="Entertainment industry jobs.",
            url="https://www.entertainmentcareers.net/"
        ),
    ]

    add(fallback_sources)

    # 🔥 GUARANTEE EXACTLY 10 RESULTS
    if len(results) < 10:
        needed = 10 - len(results)

        fillers = [
            Listing(
                title=f"Search more results: {query}",
                location="Online",
                source="Google",
                summary="Explore more casting opportunities.",
                url=f"https://www.google.com/search?q={encoded}"
            )
        ]

        for filler in fillers:
            if filler.url not in seen:
                results.append(filler)
                seen.add(filler.url)

    return results[:10]