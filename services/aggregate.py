from typing import List
from models import Listing
from sources.craigslist import search_craigslist

def aggregate_results(query: str) -> List[Listing]:
results: List[Listing] = []

# TEMP: force at least one result (so we know UI works)
results.append(
Listing(
title=f"Test listing for: {query}",
location="Las Vegas",
source="Test",
summary="Temporary test result",
url="https://example.com"
)
)

try:
results.extend(search_craigslist(query))
except Exception as e:
print("Craigslist error:", e)

return results[:10]
