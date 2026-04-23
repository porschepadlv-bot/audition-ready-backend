from fastapi import FastAPI
from models import SearchRequest, SearchResponse
from services.aggregate import aggregate_results

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    results = aggregate_results(req.prompt)
    return {"results": results}  
