from dotenv import load_dotenv
import os
import json

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SearchRequest(BaseModel):
 prompt: str

@app.post("/search")
def search(req: SearchRequest):
 completion = client.chat.completions.create(
 model=os.getenv("OPENAI_MODEL"),
 messages=[
 {
 "role": "system",
 "content": "Return audition results as a JSON array. Each item must include: title, summary, location, type, pay."
 },
 {
 "role": "user",
 "content": req.prompt
 }
 ]
 )

 content = completion.choices[0].message.content

 try:
     parsed = json.loads(content)
     return parsed
 except:
     return {"raw": content}
