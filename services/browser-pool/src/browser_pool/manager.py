from __future__ import annotations

import asyncio
import contextlib
import os
import time
import uuid
from dataclasses import dataclass
from typing import Dict, Optional

from prometheus_client import Gauge, Histogram

# Metrics
ACTIVE_LEASES = Gauge(
    "browser_pool_active_leases", "Number of active browser context leases"
)
LEASE_LATENCY = Histogram(
    "browser_pool_request_latency_seconds", "Latency of browser pool operations", ["op"]
)


@dataclass
class _Session:
    context: object
    expires_at: float


class BrowserPool:
    """Simple BrowserContext pool backed by Playwright."""

    def __init__(self, max_contexts: int = 5, ttl: float = 30.0) -> None:
        self.max_contexts = max_contexts
        self.ttl = ttl
        self._sessions: Dict[str, _Session] = {}
        self._browser = None
        self._lock = asyncio.Lock()
        self._cleanup_task: Optional[asyncio.Task[None]] = None
        if os.environ.get("BROWSER_POOL_ENABLE_CLEANUP", "1") == "1":
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def _launch_browser(self) -> None:
        if self._browser is None:
            from playwright.async_api import async_playwright  # type: ignore

            pw = await async_playwright().start()
            browser_type = os.environ.get("BROWSER", "chromium")
            self._browser = await getattr(pw, browser_type).launch()

    async def lease(self) -> str:
        start = time.time()
        async with self._lock:
            await self._launch_browser()
            if len(self._sessions) >= self.max_contexts:
                raise RuntimeError("no capacity")
            context = await self._browser.new_context()
            sid = str(uuid.uuid4())
            self._sessions[sid] = _Session(
                context=context, expires_at=time.time() + self.ttl
            )
            ACTIVE_LEASES.inc()
        LEASE_LATENCY.labels("lease").observe(time.time() - start)
        return sid

    async def release(self, session_id: str) -> None:
        start = time.time()
        async with self._lock:
            session = self._sessions.pop(session_id, None)
        if session:
            await session.context.close()
            ACTIVE_LEASES.dec()
        LEASE_LATENCY.labels("release").observe(time.time() - start)

    async def screenshot(self, session_id: str, url: str) -> bytes:
        start = time.time()
        session = self._sessions.get(session_id)
        if not session:
            raise KeyError("unknown session")
        page = await session.context.new_page()
        await page.goto(url)
        data = await page.screenshot(full_page=True)
        await page.close()
        LEASE_LATENCY.labels("screenshot").observe(time.time() - start)
        return data

    async def fetch_text(self, session_id: str, url: str) -> str:
        start = time.time()
        session = self._sessions.get(session_id)
        if not session:
            raise KeyError("unknown session")
        page = await session.context.new_page()
        await page.goto(url)
        text = await page.inner_text("body")
        await page.close()
        LEASE_LATENCY.labels("fetch_text").observe(time.time() - start)
        return text

    async def _cleanup_loop(self) -> None:
        while True:
            await asyncio.sleep(self.ttl / 2)
            now = time.time()
            expired = [sid for sid, s in self._sessions.items() if s.expires_at <= now]
            for sid in expired:
                await self.release(sid)

    async def shutdown(self) -> None:
        if self._cleanup_task:
            self._cleanup_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._cleanup_task
        if self._browser:
            await self._browser.close()
