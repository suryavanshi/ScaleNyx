from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
DOCS: List[dict[str, str]] = []


class IngestRequest(BaseModel):
    urls: List[str]


@app.post("/ingest")
def ingest(req: IngestRequest) -> dict[str, int]:
    for url in req.urls:
        DOCS.append({"url": url, "text": url})
    return {"count": len(req.urls)}


@app.get("/search")
def search(q: str, filters: str | None = None) -> dict[str, List[dict[str, str]]]:
    results = [doc for doc in DOCS if q.lower() in doc["text"].lower()]
    return {"results": results}
