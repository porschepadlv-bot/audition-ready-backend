from typing import List
from models import Listing
from urllib.parse import quote_plus

def search_craigslist(query: str) -> List[Listing]:
encoded = quote_plus(query)

return [
Listing(
title=f"Craigslist results for {query}",
location="Las Vegas, NV",
source="Craigslist",
summary="Open Craigslist results for this search.",
url=f"https://www.google.com/search?q=site%3Acraigslist.org+{encoded}"
)
]
