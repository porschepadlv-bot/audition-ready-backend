from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import json
from urllib.parse import quote_plus

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SearchRequest(BaseModel):
 prompt: str

@app.get("/")
def root():
 return {"status": "API is running"}

@app.post("/search")
def search(req: SearchRequest):
 query = req.prompt.strip()
 encoded = quote_plus(query)

 fallback_results = [
 {
 "title": f"Backstage search: {query}",
 "location": "Web",
 "url": f"https://www.backstage.com/casting/open-casting-calls/?q={encoded}"
 },
 {
 "title": f"Craigslist search: {query}",
 "location": "Web",
 "url": f"https://www.google.com/search?q=site%3Acraigslist.org+{encoded}"
 },
 {
 "title": f"Indeed search: {query}",
 "location": "Web",
 "url": f"https://www.indeed.com/jobs?q={encoded}"
 },
 {
 "title": f"Google casting search: {query}",
 "location": "Web",
 "url": f"https://www.google.com/search?q={encoded}+casting+calls"
 }
 ]

 try:
     completion = client.chat.completions.create(
 model="gpt-4o-mini",
 messages=[
 {
 "role": "system",
 "content": (
 "Return valid JSON only. No markdown, no backticks, no explanation. "
 "Return this exact shape: "
 "{\"results\":[{\"title\":\"...\",\"location\":\"...\",\"url\":\"...\"}]}. "
 "Use only real search/result links from known sites such as Backstage, "
 "Indeed, Craigslist search pages, or Google search links. "
 "Do not invent fake job listing URLs. Return at most 4 results."
 )
 },
 {
 "role": "user",
 "content": query
 }
 ]
 )

 raw = completion.choices[0].message.content

 try:
 parsed = json.loads(raw)

 if isinstance(parsed, dict) and isinstance(parsed.get("results"), list):
 cleaned = []
 for item in parsed["results"]:
 if isinstance(item, dict):
 title = str(item.get("title", "")).strip()
 location = str(item.get("location", "Web")).strip()
 url = str(item.get("url", "")).strip()
 if title and url.startswith("http"):
 cleaned.append({
 "title": title,
 "location": location or "Web",
 "url": url
 })

 if cleaned:
 return {"results": cleaned}

 return {"results": fallback_results}

 except Exception:
 return {"results": fallback_results}

 except Exception:
 return {"results": fallback_results}
