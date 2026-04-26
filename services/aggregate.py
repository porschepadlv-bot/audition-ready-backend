from sources.craigslist import search_craigslist
from sources.indeed import search_indeed
from sources.backstage import search_backstage
from typing import List
from models import Listing
from urllib.parse import urlparse


def aggregate_results(query: str) -> List[Listing]:
    results: List[tuple] = []
    seen_keys = set()

    def clean_text(value: str) -> str:
        return (value or "").strip().lower()

    def craigslist_id(url: str):
        try:
            last = urlparse(url).path.split("/")[-1]
            if last.endswith(".html"):
                post_id = last.replace(".html", "")
                if post_id.isdigit():
                    return post_id
        except Exception:
            pass
        return None

    def result_key(item: Listing) -> str:
        cl_id = craigslist_id(item.url)
        if cl_id:
            return f"craigslist-{cl_id}"

        return "|".join([
            clean_text(item.title),
            clean_text(item.location),
            clean_text(item.source),
            clean_text(item.url).split("?")[0]
        ])

    def is_bad_result(item: Listing) -> bool:
        title = clean_text(item.title)
        url = clean_text(item.url)
        source = clean_text(item.source)

        if not title or not url:
            return True

        bad_words = [
            "404",
            "not found",
            "page not found",
            "login",
            "sign in",
            "access denied",
            "forbidden"
        ]

        if any(word in title or word in url for word in bad_words):
            return True

        # Remove generic fallback/search pages pretending to be listings
        generic_sources = {
            "casting networks",
            "mandy",
            "facebook",
            "actors access",
            "casting frontier",
            "playbill",
            "entertainmentcareers"
        }

        if source in generic_sources:
            return True

        return False

    def add_results(new_results: List[Listing], priority: int):
        for item in new_results:
            if is_bad_result(item):
                continue

            key = result_key(item)

            if key in seen_keys:
                continue

            seen_keys.add(key)
            results.append((priority, item))

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

    results.sort(key=lambda x: x[0])

    final_results = [item for _, item in results]

    return final_results[:10]