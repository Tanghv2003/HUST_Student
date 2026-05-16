import json
from pathlib import Path

from HUST_Student.core.paths import STUDYSETS_DIR, STUDYSETS_JSON


def load_studysets():
    with open(STUDYSETS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def load_studyset_detail(file_path: str):
    resolved = STUDYSETS_DIR / Path(file_path)
    with open(resolved, "r", encoding="utf-8") as f:
        return json.load(f)