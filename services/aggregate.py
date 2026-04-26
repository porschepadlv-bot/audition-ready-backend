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

    backup_sources = [
        Listing(
            title=f"Backstage Casting: {query}",
            location="Nationwide",
            source="Backstage",
            summary="Browse matching casting calls on Backstage. Account signup may be required.",
            url="https://www.backstage.com/casting/"
        ),
        Listing(
            title=f"Facebook Groups: {query}",
            location="Local / Online",
            source="Facebook",
            summary="Find local casting calls in Facebook groups.",
            url=f"https://www.facebook.com/search/groups/?q={encoded}"
        ),
        Listing(
            title="Auditions Free",
            location="Nationwide",
            source="Auditions Free",
            summary="Indie films, student projects, and low-budget casting calls. Free to browse.",
            url="https://www.auditionsfree.com/"
        ),
        Listing(
            title="Casting Call Hub",
            location="Nationwide",
            source="Casting Call Hub",
            summary="Browse acting, modeling, and casting opportunities across multiple categories.",
            url="https://www.castingcallhub.com/"
        ),
        Listing(
            title="Local Theater Auditions",
            location="Local",
            source="Community Theater",
            summary="Search local theater companies and community productions for auditions in your city.",
            url=f"https://www.google.com/search?q={encoded}+community+theater+auditions"
        ),
        Listing(
            title="Film School Casting Calls",
            location="Local / Nationwide",
            source="Film School",
            summary="Student films casting actors for experience and credits.",
            url=f"https://www.google.com/search?q={encoded}+film+school+casting+calls"
        ),
        Listing(
            title="NYCastings",
            location="Nationwide",
            source="NYCastings",
            summary="Casting calls and acting jobs across film, TV, and theater.",
            url="https://www.nycastings.com/"
        ),
        Listing(
            title="Playbill Jobs",
            location="Nationwide",
            source="Playbill",
            summary="Theater auditions and Broadway-related casting opportunities.",
            url="https://www.playbill.com/jobs"
        ),
    ]

    add(backup_sources)

    return results[:20]