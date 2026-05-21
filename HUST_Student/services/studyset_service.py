import json
from pathlib import Path

from HUST_Student.core.paths import STUDYSETS_DIR, STUDYSETS_JSON


def load_studysets_raw() -> dict:
    with open(STUDYSETS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save_studysets(data: dict) -> None:
    with open(STUDYSETS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_studyset_detail(file_path: str):
    resolved = STUDYSETS_DIR / Path(file_path)
    with open(resolved, "r", encoding="utf-8") as f:
        return json.load(f)


def _enrich_sets(sets: list) -> list:
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
    return enriched


def load_studysets() -> dict:
    raw = load_studysets_raw()
    return {folder_path: _enrich_sets(sets) for folder_path, sets in raw.items()}


def get_studysets_for_path(path_key: str) -> list[dict]:
    return load_studysets().get(path_key, [])


def add_studyset(path_key: str, title: str, file_path: str) -> bool:
    title = title.strip()
    file_path = file_path.strip()
    if not path_key or not title or not file_path:
        return False

    data = load_studysets_raw()
    sets = data.setdefault(path_key, [])
    if any(s.get("title") == title for s in sets):
        return False

    sets.append({"title": title, "file": file_path})
    save_studysets(data)
    return True


def remove_studyset(path_key: str, title: str) -> bool:
    data = load_studysets_raw()
    sets = data.get(path_key, [])
    new_sets = [s for s in sets if s.get("title") != title]
    if len(new_sets) == len(sets):
        return False
    if new_sets:
        data[path_key] = new_sets
    else:
        del data[path_key]
    save_studysets(data)
    return True


def rename_studyset_path_prefix(old_prefix: str, new_prefix: str) -> None:
    """Đổi key trong studysets.json khi đổi tên / di chuyển folder."""
    if old_prefix == new_prefix:
        return
    data = load_studysets_raw()
    updated: dict = {}
    for key, sets in data.items():
        if key == old_prefix:
            updated[new_prefix] = sets
        elif key.startswith(old_prefix + "/"):
            updated[new_prefix + key[len(old_prefix) :]] = sets
        else:
            updated[key] = sets
    save_studysets(updated)


def delete_studysets_under(path_key: str) -> None:
    """Xóa mọi bài giảng thuộc folder và folder con."""
    data = load_studysets_raw()
    keys_to_remove = [
        k for k in data if k == path_key or k.startswith(path_key + "/")
    ]
    for k in keys_to_remove:
        del data[k]
    save_studysets(data)
