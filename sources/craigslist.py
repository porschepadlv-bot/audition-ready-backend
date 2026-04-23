try:
    cl = search_craigslist(query)
    print("CRAIGSLIST RESULTS:", cl)
    results.extend(cl)
except Exception as e:
    print("Craigslist error:", e)