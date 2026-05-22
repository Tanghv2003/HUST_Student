"""
studyset_service.py — CRUD bài giảng trong studysets.json.

Mỗi entry trong studysets.json:
  "path_key": [{"title": "...", "file": "...", "terms": N}]
"""

import json
from pathlib import Path

from HUST_Student.core.paths import STUDYSETS_DIR, STUDYSETS_JSON


# ══════════════════════════════════════════════════════════════════
# I/O
# ══════════════════════════════════════════════════════════════════

def load_studysets_raw() -> dict:
    try:
        with open(STUDYSETS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_studysets(data: dict) -> None:
    with open(STUDYSETS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_studyset_detail(file_path: str) -> list:
    resolved = STUDYSETS_DIR / Path(file_path)
    with open(resolved, "r", encoding="utf-8") as f:
        return json.load(f)


# ══════════════════════════════════════════════════════════════════
# ENRICH (đếm số term từ file JSON nếu chưa có)
# ══════════════════════════════════════════════════════════════════

def _enrich_sets(sets: list) -> list:
    enriched = []
    for item in sets:
        entry = dict(item)
        if not entry.get("terms"):
            try:
                detail = load_studyset_detail(entry["file"])
                entry["terms"] = len(detail) if isinstance(detail, list) else 0
            except Exception:
                entry["terms"] = 0
        enriched.append(entry)
    return enriched


def load_studysets() -> dict:
    raw = load_studysets_raw()
    return {folder_path: _enrich_sets(sets) for folder_path, sets in raw.items()}


def get_studysets_for_path(path_key: str) -> list[dict]:
    return load_studysets().get(path_key, [])


# ══════════════════════════════════════════════════════════════════
# CRUD
# ══════════════════════════════════════════════════════════════════

def add_studyset(path_key: str, title: str, file_path: str) -> tuple[bool, str]:
    """Thêm bài giảng vào path_key. Trả về (success, error_message)."""
    title = title.strip()
    file_path = file_path.strip()
    if not path_key:
        return False, "path_key không được để trống."
    if not title:
        return False, "Tên bài giảng không được để trống."
    if not file_path:
        return False, "Đường dẫn file không được để trống."

    data = load_studysets_raw()
    sets = data.setdefault(path_key, [])
    if any(s.get("title") == title for s in sets):
        return False, f"Bài giảng '{title}' đã tồn tại."

    sets.append({"title": title, "file": file_path})
    save_studysets(data)
    return True, ""


def remove_studyset(path_key: str, title: str) -> tuple[bool, str]:
    """Xoá bài giảng theo title. Trả về (success, error_message)."""
    data = load_studysets_raw()
    sets = data.get(path_key, [])
    new_sets = [s for s in sets if s.get("title") != title]
    if len(new_sets) == len(sets):
        return False, f"Không tìm thấy bài giảng '{title}'."
    if new_sets:
        data[path_key] = new_sets
    elif path_key in data:
        del data[path_key]
    save_studysets(data)
    return True, ""


def rename_studyset(path_key: str, old_title: str, new_title: str) -> tuple[bool, str]:
    """Đổi tên bài giảng."""
    new_title = new_title.strip()
    if not new_title:
        return False, "Tên mới không được để trống."
    data = load_studysets_raw()
    sets = data.get(path_key, [])
    if not any(s.get("title") == old_title for s in sets):
        return False, f"Không tìm thấy bài giảng '{old_title}'."
    if new_title != old_title and any(s.get("title") == new_title for s in sets):
        return False, f"Bài giảng '{new_title}' đã tồn tại."
    for s in sets:
        if s.get("title") == old_title:
            s["title"] = new_title
    save_studysets(data)
    return True, ""


def rename_studyset_path_prefix(old_prefix: str, new_prefix: str) -> None:
    """Đổi key trong studysets.json khi đổi tên/di chuyển folder."""
    if old_prefix == new_prefix:
        return
    data = load_studysets_raw()
    updated: dict = {}
    for key, sets in data.items():
        if key == old_prefix:
            updated[new_prefix] = sets
        elif key.startswith(old_prefix + "/"):
            updated[new_prefix + key[len(old_prefix):]] = sets
        else:
            updated[key] = sets
    save_studysets(updated)


def delete_studysets_under(path_key: str) -> None:
    """Xoá mọi bài giảng thuộc folder và folder con."""
    data = load_studysets_raw()
    keys_to_remove = [
        k for k in data if k == path_key or k.startswith(path_key + "/")
    ]
    for k in keys_to_remove:
        del data[k]
    save_studysets(data)


def move_studyset(src_path: str, dst_path: str, title: str) -> tuple[bool, str]:
    """Di chuyển bài giảng từ src_path sang dst_path."""
    data = load_studysets_raw()
    src_sets = data.get(src_path, [])
    item = next((s for s in src_sets if s.get("title") == title), None)
    if not item:
        return False, f"Không tìm thấy bài giảng '{title}'."
    dst_sets = data.get(dst_path, [])
    if any(s.get("title") == title for s in dst_sets):
        return False, f"Bài giảng '{title}' đã tồn tại tại đích."
    # Remove from src
    data[src_path] = [s for s in src_sets if s.get("title") != title]
    if not data[src_path]:
        del data[src_path]
    # Add to dst
    dst_sets.append(item)
    data[dst_path] = dst_sets
    save_studysets(data)
    return True, ""