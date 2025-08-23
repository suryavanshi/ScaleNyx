"""Browser pool client stub."""


def screenshot(url: str) -> str:
    """Return a fake path to a screenshot for the URL."""
    return f"/tmp/screenshot_{hash(url)}.png"
