from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
 prompt: str

class Listing(BaseModel):
 title: str
 location: str
 source: str
 summary: str
 url: str

class SearchResponse(BaseModel):
 results: List[Listing]

