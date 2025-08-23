from typing import List

import requests

from .schemas import SearchResult


def search(
    base_url: str, query: str, provider: str, service: str
) -> List[SearchResult]:
    params = {"q": query, "filters": f"provider:{provider},service:{service}"}
    resp = requests.get(f"{base_url}/search", params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [SearchResult(**item) for item in data.get("results", [])]
