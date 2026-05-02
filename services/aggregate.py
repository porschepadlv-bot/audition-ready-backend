from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from sources.actorsaccess import search_actors_access
from sources.castingnetworks import search_casting_networks
from sources.castingfrontier import search_casting_frontier
from sources.mandy import search_mandy
from sources.entertainmentcareers import search_entertainment_careers
from sources.projectcasting import search_project_casting

from urllib.parse import quote_plus
from models import Listing


MAJOR = "Major Platforms"
LOCAL = "Local Listings"
HIDDEN = "Hidden Opportunities"


def listing_to_dict(item, category):
    return {
        "title": item.title,
        "location": item.location,
        "source": item.source,
        "summary": item.summary,
        "url": item.url,
        "category": category
    }


def aggregate_results(query: str):
    results = []
    seen = set()
    encoded = quote_plus(query)

    def add(items, category):
        for item in items:
            if not item.url:
                continue

            key = item.url.strip().lower().replace("https://www.", "https://")
            if key in seen:
                continue

            seen.add(key)
            results.append(listing_to_dict(item, category))

    major_sources = [
        ("Indeed", search_indeed),
        ("Actors Access", search_actors_access),
        ("Backstage", search_backstage),
        ("Casting Networks", search_casting_networks),
        ("Casting Frontier", search_casting_frontier),
        ("Mandy", search_mandy),
        ("Entertainment Careers", search_entertainment_careers),
    ]

    hidden_sources = [
        ("Project Casting", search_project_casting),
    ]

    local_sources = [
        ("Craigslist", search_craigslist),
    ]

    for label, fn in major_sources:
        try:
            add(fn(query), MAJOR)
        except Exception as e:
            print(f"{label} error:", e)

    for label, fn in hidden_sources:
        try:
            add(fn(query), HIDDEN)
        except Exception as e:
            print(f"{label} error:", e)

    for label, fn in local_sources:
        try:
            add(fn(query), LOCAL)
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
            location="Las Vegas / Local",
            source="Community Theater",
            summary="Browse local theater audition pages, including UNLV Callboard and Las Vegas theater opportunities.",
            url="https://callboard.sites.unlv.edu/auditions/"
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

    add(backup_sources[:1], MAJOR)
    add(backup_sources[1:6], HIDDEN)
    add(backup_sources[6:], MAJOR)

    return results[:16]
