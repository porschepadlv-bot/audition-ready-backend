from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SearchRequest(BaseModel):
 prompt: str

@app.get("/")
def root():
 return {"status": "API is running"}

@app.post("/search")
def search(req: SearchRequest):
 return {
 "result": [
 {
 "title": "Sample Acting Job 1",
 "summary": f"Search received: {req.prompt}",
 "location": "Las Vegas, NV"
 },
 {
 "title": "Sample Acting Job 2",
 "summary": "Backend is working correctly.",
 "location": "Henderson, NV"
 }
 ]
 }
