from pydantic import BaseModel


class SearchResult(BaseModel):
    url: str
    snippet: str
