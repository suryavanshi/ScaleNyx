from __future__ import annotations

import io
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from prometheus_client import make_asgi_app

try:  # optional OpenTelemetry instrumentation
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except Exception:  # pragma: no cover - optional
    FastAPIInstrumentor = None

from .manager import BrowserPool

MAX_CONTEXTS = int(os.environ.get("MAX_CONTEXTS", "5"))
TTL = float(os.environ.get("SESSION_TTL", "30"))

pool = BrowserPool(max_contexts=MAX_CONTEXTS, ttl=TTL)
app = FastAPI()
if FastAPIInstrumentor:  # pragma: no cover
    FastAPIInstrumentor.instrument_app(app)
app.mount("/metrics", make_asgi_app())


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/lease")
async def lease() -> dict[str, str]:
    try:
        session_id = await pool.lease()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"session": session_id}


@app.post("/release/{session_id}")
async def release(session_id: str) -> dict[str, str]:
    await pool.release(session_id)
    return {"status": "released"}


@app.get("/screenshot")
async def screenshot(session: str, url: str) -> StreamingResponse:
    data = await pool.screenshot(session, url)
    return StreamingResponse(io.BytesIO(data), media_type="image/png")


@app.get("/fetchText")
async def fetch_text(session: str, url: str) -> dict[str, str]:
    text = await pool.fetch_text(session, url)
    return {"text": text}
