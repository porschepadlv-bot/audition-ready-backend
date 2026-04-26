from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from sources.actorsaccess import search_actors_access
from sources.castingnetworks import search_casting_networks
from sources.castingfrontier import search_casting_frontier
from sources.mandy import search_mandy
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

            key = item.url.strip().lower().replace("https://www.", "https://")

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
        add(search_actors_access(query))
    except Exception as e:
        print("Actors Access error:", e)

    try:
        add(search_casting_networks(query))
    except Exception as e:
        print("Casting Networks error:", e)

    try:
        add(search_casting_frontier(query))
    except Exception as e:
        print("Casting Frontier error:", e)

    try:
        add(search_mandy(query))
    except Exception as e:
        print("Mandy error:", e)

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
            title="Playbill Jobs",
            location="Nationwide",
            source="Playbill",
            summary="Theater auditions and casting opportunities.",
            url="https://www.playbill.com/jobs"
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