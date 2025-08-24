import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from knowledge.api.main import Document, ingest, search  # noqa: E402


def test_ingest_and_search():
    docs = [
        Document(
            url="http://a",
            provider="aws",
            service="s3",
            last_modified=datetime.utcnow(),
            text="public bucket policy",
        ),
        Document(
            url="http://b",
            provider="aws",
            service="iam",
            last_modified=datetime.utcnow(),
            text="iam policy",
        ),
    ]
    ingest(docs)
    res = search(q="bucket", provider="aws", service="s3", limit=5)
    assert res["results"][0]["url"] == "http://a"
