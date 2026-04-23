from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SearchRequest(BaseModel):
 prompt: str

@app.get("/")
def root():
 return {"status": "API is running"}

@app.post("/search")
def search(req: SearchRequest):
 completion = client.chat.completions.create(
 model="gpt-4o-mini",
 messages=[
 {
 "role": "system",
 "content": "Return acting auditions in a simple line-by-line list with one item per line."
 },
 {
 "role": "user",
 "content": req.prompt
 }
 ]
 )

 raw = completion.choices[0].message.content

 items = [line.strip() for line in raw.split("\n") if line.strip()]

 return {
 "results": items
 }
