import time
from typing import List

import requests
from prometheus_client import Histogram

from .schemas import SearchResult

KB_CLIENT_LATENCY = Histogram(
    "kb_client_search_latency_seconds", "Knowledge base client search latency"
)


def search(
    base_url: str, query: str, provider: str, service: str
) -> List[SearchResult]:
    params = {"q": query, "provider": provider, "service": service}
    start = time.time()
    resp = requests.get(f"{base_url}/search", params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    KB_CLIENT_LATENCY.observe(time.time() - start)
    return [SearchResult(**item) for item in data.get("results", [])]
