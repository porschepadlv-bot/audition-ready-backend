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
 model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
 messages=[
 {
 "role": "system",
 "content": (
 "Return audition results as a pure JSON array only. "
 "No markdown. No backticks. No explanation. "
 "Each item must include exactly these keys: "
 "title, summary, location."
 )
 },
 {
 "role": "user",
 "content": req.prompt
 }
 ]
 )

 raw = completion.choices[0].message.content.strip()

 cleaned = raw.replace("```json", "").replace("```", "").strip()

 try:
 parsed = json.loads(cleaned)
 if isinstance(parsed, list):
 return {"result": parsed}
 else:
 return {"result": []}
 except Exception as e:
 return {
 "result": [],
 "error": str(e),
 "raw": raw
 }
