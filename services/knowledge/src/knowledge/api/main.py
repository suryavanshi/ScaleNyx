from __future__ import annotations

import time
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Query
from prometheus_client import Histogram, make_asgi_app
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer

try:  # optional OpenTelemetry instrumentation
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except Exception:  # pragma: no cover - optional
    FastAPIInstrumentor = None

app = FastAPI()
if FastAPIInstrumentor:  # pragma: no cover
    FastAPIInstrumentor.instrument_app(app)
app.mount("/metrics", make_asgi_app())


class Document(BaseModel):
    url: str
    provider: str
    service: str
    last_modified: datetime
    text: str


DOCS: List[Document] = []
_VECTOR = TfidfVectorizer()
_MATRIX = None

SEARCH_LATENCY = Histogram("kb_search_latency_seconds", "Knowledge base search latency")


def _reindex() -> None:
    global _MATRIX
    if DOCS:
        texts = [d.text for d in DOCS]
        _MATRIX = _VECTOR.fit_transform(texts)
    else:  # pragma: no cover - no documents
        _MATRIX = None


@app.post("/ingest")
def ingest(docs: List[Document]) -> dict[str, int]:
    DOCS.extend(docs)
    _reindex()
    return {"count": len(docs)}


@app.post("/reindex")
def reindex() -> dict[str, str]:
    _reindex()
    return {"status": "ok"}


@app.get("/search")
def search(
    q: str,
    provider: Optional[str] = Query(None),
    service: Optional[str] = Query(None),
    limit: int = Query(5),
) -> dict[str, List[dict[str, str]]]:
    start = time.time()
    if not DOCS:
        return {"results": []}
    if _MATRIX is None:
        _reindex()
    filtered_idx = [
        i
        for i, d in enumerate(DOCS)
        if (provider is None or d.provider == provider)
        and (service is None or d.service == service)
    ]
    if not filtered_idx:
        return {"results": []}
    subset = _MATRIX[filtered_idx]
    q_vec = _VECTOR.transform([q])
    sims = (subset @ q_vec.T).toarray().ravel()
    scored = sorted(zip(filtered_idx, sims), key=lambda x: x[1], reverse=True)[:limit]
    results = [
        {
            "url": DOCS[i].url,
            "provider": DOCS[i].provider,
            "service": DOCS[i].service,
            "last_modified": DOCS[i].last_modified.isoformat(),
            "snippet": DOCS[i].text[:200],
        }
        for i, _ in scored
    ]
    SEARCH_LATENCY.observe(time.time() - start)
    return {"results": results}
