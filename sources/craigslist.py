def search_craigslist(query: str) -> List[Listing]:
    listings: List[Listing] = []

    listings.extend(scrape_category("ggg", query))
    listings.extend(scrape_category("tlg", query))

    # 🔥 remove duplicates by URL
    seen = set()
    unique = []

    for item in listings:
        if item.url not in seen:
            seen.add(item.url)
            unique.append(item)

    if unique:
        return unique[:5]

    encoded = quote_plus(query)
    return [
        Listing(
            title=f"Craigslist results: {query}",
            location="Las Vegas",
            source="Craigslist",
            summary="Tap to view Craigslist search results.",
            url=f"https://lasvegas.craigslist.org/search/ggg?query={encoded}"
        )
    ]