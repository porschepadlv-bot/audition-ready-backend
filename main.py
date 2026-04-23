from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import quote_plus

app = FastAPI()

class SearchRequest(BaseModel):
 prompt: str

@app.get("/")
def root():
 return {"status": "API is running"}

@app.post("/search")
def search(req: SearchRequest):
 query = req.prompt.strip()
 encoded = quote_plus(query)

 return {
 "results": [
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
 }
