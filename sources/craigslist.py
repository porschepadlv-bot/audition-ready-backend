try:
    cl = search_craigslist(query)
    print("CRAIGSLIST SUCCESS:", cl)
    results.extend(cl)
except Exception as e:
    print("🔥 CRAIGSLIST ERROR:", str(e))
    raise e   # 👈 IMPORTANT: crash so we SEE it