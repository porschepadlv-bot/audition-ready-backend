from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from sources.actorsaccess import search_actors_access
from sources.castingnetworks import search_casting_networks
from sources.castingfrontier import search_casting_frontier
from sources.mandy import search_mandy
from sources.entertainmentcareers import search_entertainment_careers
from sources.projectcasting import search_project_casting
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

    for label, fn in [
        ("Backstage", search_backstage),
        ("Indeed", search_indeed),
        ("Actors Access", search_actors_access),
        ("Casting Networks", search_casting_networks),
        ("Casting Frontier", search_casting_frontier),
        ("Mandy", search_mandy),
        ("Entertainment Careers", search_entertainment_careers),
        ("Project Casting", search_project_casting),
        ("Craigslist", search_craigslist),
    ]:
        try:
            add(fn(query))
        except Exception as e:
            print(f"{label} error:", e)

    fallback_sources = [
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