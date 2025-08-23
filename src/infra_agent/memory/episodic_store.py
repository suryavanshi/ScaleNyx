import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

TRACES_DIR = Path(__file__).parent / "traces"


def write_trace(name: str, steps: List[Dict[str, Any]]) -> Path:
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    path = TRACES_DIR / f"{name}_{datetime.utcnow().isoformat()}.json"
    with path.open("w") as f:
        json.dump(steps, f, indent=2)
    return path
