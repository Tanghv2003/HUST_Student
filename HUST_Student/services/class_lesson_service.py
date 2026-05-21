import json
from pathlib import Path

from HUST_Student.core.paths import CLASS_LESSONS_DIR, CLASS_LESSONS_JSON


def load_class_lessons_raw() -> dict:
    try:
        with open(CLASS_LESSONS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_class_lessons(data: dict) -> None:
    with open(CLASS_LESSONS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_lesson_detail(file_path: str):
    resolved = CLASS_LESSONS_DIR / Path(file_path)
    with open(resolved, "r", encoding="utf-8") as f:
        return json.load(f)


def _enrich_lessons(lessons: list) -> list:
    enriched = []
    for item in lessons:
        entry = dict(item)
        if "terms" not in entry or entry.get("terms", 0) == 0:
            try:
                detail = load_lesson_detail(entry["file"])
                if isinstance(detail, list):
                    entry["terms"] = len(detail)
                elif isinstance(detail, dict):
                    entry["terms"] = len(detail.get("words", detail.get("items", [])))
                else:
                    entry["terms"] = 0
            except Exception:
                entry["terms"] = 0
        enriched.append(entry)
    return enriched


def load_class_lessons() -> dict:
    raw = load_class_lessons_raw()
    return {path: _enrich_lessons(items) for path, items in raw.items()}


def get_lessons_for_path(path_key: str) -> list[dict]:
    return load_class_lessons().get(path_key, [])


def add_lesson(path_key: str, title: str, file_path: str) -> bool:
    title = title.strip()
    file_path = file_path.strip()
    if not path_key or not title or not file_path:
        return False

    data = load_class_lessons_raw()
    lessons = data.setdefault(path_key, [])
    if any(x.get("title") == title for x in lessons):
        return False

    lessons.append({"title": title, "file": file_path})
    save_class_lessons(data)
    return True


def remove_lesson(path_key: str, title: str) -> bool:
    data = load_class_lessons_raw()
    lessons = data.get(path_key, [])
    new_lessons = [x for x in lessons if x.get("title") != title]
    if len(new_lessons) == len(lessons):
        return False
    if new_lessons:
        data[path_key] = new_lessons
    else:
        del data[path_key]
    save_class_lessons(data)
    return True


def rename_lesson_path_prefix(old_prefix: str, new_prefix: str) -> None:
    if old_prefix == new_prefix:
        return
    data = load_class_lessons_raw()
    updated: dict = {}
    for key, lessons in data.items():
        if key == old_prefix:
            updated[new_prefix] = lessons
        elif key.startswith(old_prefix + "/"):
            updated[new_prefix + key[len(old_prefix) :]] = lessons
        else:
            updated[key] = lessons
    save_class_lessons(updated)


def delete_lessons_under(path_key: str) -> None:
    data = load_class_lessons_raw()
    keys = [k for k in data if k == path_key or k.startswith(path_key + "/")]
    for k in keys:
        del data[k]
    save_class_lessons(data)
