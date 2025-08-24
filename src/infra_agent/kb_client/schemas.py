from pydantic import BaseModel


class SearchResult(BaseModel):
    url: str
    provider: str
    service: str
    last_modified: str
    snippet: str | None = None
