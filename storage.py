# storage.py
import json, hashlib
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "survey.ndjson"
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def append_json_line(row: dict) -> bool:
    """Append one JSON object per line. Drop exact duplicates by submission_id."""
    sid = row.get("submission_id")
    if sid and DATA_PATH.exists():
        with DATA_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    j = json.loads(line)
                except Exception:
                    continue
                if j.get("submission_id") == sid:
                    return False
    with DATA_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return True
