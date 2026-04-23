from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import json

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
 "content": "Return audition results as a pure JSON array. No backticks. No explanation."
 },
 {
 "role": "user",
 "content": req.prompt
 }
 ]
 )

 raw = completion.choices[0].message.content

 try:
 parsed = json.loads(raw)
 return parsed
 except Exception:
 return {"error": "Invalid JSON from AI", "raw": raw}