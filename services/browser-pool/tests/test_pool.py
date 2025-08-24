import asyncio
import sys
from pathlib import Path

import pytest  # noqa: F401

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from browser_pool.manager import BrowserPool  # noqa: E402


class DummyPage:
    def __init__(self) -> None:
        self.url = None

    async def goto(self, url: str) -> None:  # pragma: no cover - simple stub
        self.url = url

    async def screenshot(self, full_page: bool = True) -> bytes:
        return b"img"

    async def inner_text(self, selector: str) -> str:
        return "text"

    async def close(self) -> None:
        pass


class DummyContext:
    async def new_page(self) -> DummyPage:
        return DummyPage()

    async def close(self) -> None:
        pass


class DummyBrowser:
    async def new_context(self) -> DummyContext:
        return DummyContext()

    async def close(self) -> None:  # pragma: no cover - simple stub
        pass


def test_lease_and_release(monkeypatch):
    async def _run() -> None:
        pool = BrowserPool(max_contexts=1, ttl=1)

        async def fake_launch(self) -> None:
            self._browser = DummyBrowser()

        monkeypatch.setattr(BrowserPool, "_launch_browser", fake_launch)

        sid = await pool.lease()
        assert sid in pool._sessions
        img = await pool.screenshot(sid, "http://example.com")
        assert img == b"img"
        text = await pool.fetch_text(sid, "http://example.com")
        assert text == "text"
        await pool.release(sid)
        assert sid not in pool._sessions
        await pool.shutdown()

    asyncio.run(_run())
