from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from typing import List
from models import Listing
from urllib.parse import quote_plus


def aggregate_results(query: str) -> List[Listing]:
    results: List[Listing] = []
    seen = set()
    encoded = quote_plus(query)

    def add(items: List[Listing]):
        for item in items:
            if not item.url:
                continue

            key = item.url.strip().lower()

            if key in seen:
                continue

            seen.add(key)
            results.append(item)

    try:
        add(search_backstage(query))
    except Exception as e:
        print("Backstage error:", e)

    try:
        add(search_indeed(query))
    except Exception as e:
        print("Indeed error:", e)

    try:
        add(search_craigslist(query))
    except Exception as e:
        print("Craigslist error:", e)

    fallback_sources = [
        Listing(
            title=f"Backstage Casting: {query}",
            location="Nationwide",
            source="Backstage",
            summary="Browse matching casting calls on Backstage. Sign up may be required.",
            url="https://www.backstage.com/casting/"
        ),
        Listing(
            title=f"Indeed jobs: {query}",
            location="Nationwide",
            source="Indeed",
            summary="Browse matching job results on Indeed. Sign up may be required.",
            url=f"https://www.indeed.com/jobs?q={encoded}"
        ),
        Listing(
            title=f"Facebook Groups: {query}",
            location="Local / Online",
            source="Facebook",
            summary="Find local casting calls in Facebook groups.",
            url=f"https://www.facebook.com/search/groups/?q={encoded}"
        ),
        Listing(
            title="Actors Access",
            location="Nationwide",
            source="Actors Access",
            summary="Professional casting breakdowns and auditions.",
            url="https://actorsaccess.com/"
        ),
        Listing(
            title="Playbill Jobs",
            location="Nationwide",
            source="Playbill",
            summary="Theater auditions and casting opportunities.",
            url="https://www.playbill.com/jobs"
        ),
        Listing(
            title="Mandy Casting",
            location="Nationwide",
            source="Mandy",
            summary="Film, TV, and commercial casting jobs.",
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
            summary="Online casting platform for actors and models.",
            url="https://www.castingfrontier.com/"
        ),
        Listing(
            title="Entertainment Careers",
            location="Nationwide",
            source="EntertainmentCareers",
            summary="Entertainment industry jobs and internships.",
            url="https://www.entertainmentcareers.net/"
        ),
        Listing(
            title="NYCastings",
            location="Nationwide",
            source="NYCastings",
            summary="Casting calls and acting jobs.",
            url="https://www.nycastings.com/"
        ),
        Listing(
            title="Casting Call Hub",
            location="Nationwide",
            source="Casting Call Hub",
            summary="Browse acting, modeling, and casting opportunities.",
            url="https://www.castingcallhub.com/"
        )
    ]

    add(fallback_sources)

    return results[:10]