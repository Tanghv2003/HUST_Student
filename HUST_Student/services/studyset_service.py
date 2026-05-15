import json

from HUST_Student.core.paths import STUDYSETS_DIR, STUDYSETS_JSON


def load_studysets():
    with open(STUDYSETS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def load_studyset_detail(file_name: str):
    file_path = STUDYSETS_DIR / file_name
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
