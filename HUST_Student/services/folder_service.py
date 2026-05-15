import json

from HUST_Student.core.paths import FOLDERS_JSON


def load_folders():
    with open(FOLDERS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save_folders(data):
    with open(FOLDERS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
