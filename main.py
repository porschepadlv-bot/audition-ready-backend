from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from services.aggregate import aggregate_results


app = FastAPI()


# Request model (fixes your 422 error)
class SearchRequest(BaseModel):
    prompt: str


# Response model (optional but clean)
class Listing(BaseModel):
    title: str
    location: str
    source: str
    summary: str
    url: str


@app.get("/")
def root():
    return {"message": "Audition Ready API is live"}


@app.post("/search", response_model=dict)
def search_jobs(request: SearchRequest):
    try:
        results = aggregate_results(request.prompt)

        return {
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))