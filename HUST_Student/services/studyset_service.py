import json
from pathlib import Path

from HUST_Student.core.paths import STUDYSETS_DIR, STUDYSETS_JSON


def load_studysets():
    with open(STUDYSETS_JSON, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # Pre-populate `terms` count from each detail file
    result = {}
    for folder_path, sets in raw.items():
        enriched = []
        for item in sets:
            entry = dict(item)
            if "terms" not in entry or entry.get("terms", 0) == 0:
                try:
                    detail = load_studyset_detail(entry["file"])
                    entry["terms"] = len(detail)
                except Exception:
                    entry["terms"] = 0
            enriched.append(entry)
        result[folder_path] = enriched
    return result


def load_studyset_detail(file_path: str):
    resolved = STUDYSETS_DIR / Path(file_path)
    with open(resolved, "r", encoding="utf-8") as f:
        return json.load(f)