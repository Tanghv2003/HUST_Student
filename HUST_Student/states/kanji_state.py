import json
from pathlib import Path
from pydantic import BaseModel

import reflex as rx


def _load_kanji_data() -> list[dict]:
    """Load kanji N5 data from JSON file."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "kanji_n5.json"
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _load_classes_data() -> dict:
    """Load classes tree data from JSON file."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "classes.json"
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Fallback structure nếu file chưa tồn tại
        return {
            "Tiếng Nhật N5": {
                "icon": "graduation-cap",
                "color": "#23B26D",
                "students": 42,
                "classes": {
                    "Nhóm A": {
                        "icon": "users",
                        "color": "#23B26D",
                        "students": 15,
                        "classes": {}
                    },
                    "Nhóm B": {
                        "icon": "users",
                        "color": "#23B26D",
                        "students": 27,
                        "classes": {}
                    }
                }
            },
            "Toeic 700+": {
                "icon": "graduation-cap",
                "color": "#4257B2",
                "students": 28,
                "classes": {
                    "Listening": {
                        "icon": "headphones",
                        "color": "#4257B2",
                        "students": 28,
                        "classes": {}
                    },
                    "Reading": {
                        "icon": "book-open",
                        "color": "#4257B2",
                        "students": 28,
                        "classes": {}
                    }
                }
            },
            "Kanji N4": {
                "icon": "graduation-cap",
                "color": "#E879F9",
                "students": 35,
                "classes": {}
            },
            "Ngữ pháp N3": {
                "icon": "graduation-cap",
                "color": "#FF9B37",
                "students": 19,
                "classes": {}
            }
        }


class KanjiItem(BaseModel):
    kanji: str = ""
    meaning: str = ""
    onyomi: str = ""
    kunyomi: str = ""
    strokes: int = 0
    lesson: int = 1
    lesson_theme: str = ""


class KanjiState(rx.State):
    all_kanji: list[KanjiItem] = []
    selected_kanji: KanjiItem | None = None
    show_detail: bool = False
    current_lesson_filter: int = 0  # 0 = all

    def load_kanji(self):
        raw = _load_kanji_data()
        items = []
        seen = set()
        for d in raw:
            key = (d.get("kanji", ""), d.get("lesson", 1))
            if key in seen:
                continue
            seen.add(key)
            items.append(
                KanjiItem(
                    kanji=d.get("kanji", ""),
                    meaning=d.get("meaning", ""),
                    onyomi=d.get("onyomi", ""),
                    kunyomi=d.get("kunyomi", ""),
                    strokes=d.get("strokes", 0),
                    lesson=d.get("lesson", 1),
                    lesson_theme=d.get("lesson_theme", ""),
                )
            )
        self.all_kanji = items

    def select_kanji(self, kanji_char: str, lesson: int):
        for k in self.all_kanji:
            if k.kanji == kanji_char and k.lesson == lesson:
                self.selected_kanji = k
                self.show_detail = True
                break

    def close_detail(self):
        self.show_detail = False
        self.selected_kanji = None

    def set_lesson_filter(self, lesson: int):
        self.current_lesson_filter = lesson

    @rx.var
    def lessons(self) -> list[int]:
        seen = []
        for k in self.all_kanji:
            if k.lesson not in seen:
                seen.append(k.lesson)
        return sorted(seen)

    @rx.var
    def filtered_kanji(self) -> list[KanjiItem]:
        if self.current_lesson_filter == 0:
            return self.all_kanji
        return [k for k in self.all_kanji if k.lesson == self.current_lesson_filter]

    @rx.var
    def lesson_groups(self) -> list[dict]:
        groups: dict[int, dict] = {}
        for k in self.all_kanji:
            if k.lesson not in groups:
                groups[k.lesson] = {
                    "lesson": k.lesson,
                    "theme": k.lesson_theme,
                    "items": [],
                }
            groups[k.lesson]["items"].append(k.dict())
        return [groups[ln] for ln in sorted(groups.keys())]


class ClassesTabState(rx.State):
    active_tab: str = "lop_hoc"  # "lop_hoc" | "kanji"

    def set_tab(self, tab: str):
        self.active_tab = tab


class ClassTreeState(rx.State):
    """Cây lớp học sidebar — reactive với classes.json & class_lessons.json."""

    open_classes: list[str] = []
    current_path_key: str = ""
    current_class: str = ""
    all_sidebar_rows: list[dict] = []
    visible_sidebar_rows: list[dict] = []

    def _refresh_visible(self):
        open_set = set(self.open_classes)
        self.visible_sidebar_rows = [
            row
            for row in self.all_sidebar_rows
            if row["level"] == 0 or row["parent_tree_key"] in open_set
        ]

    def reload_class_tree(self):
        from HUST_Student.services.class_service import build_class_sidebar_rows, load_classes
        from HUST_Student.services.class_lesson_service import load_class_lessons

        classes = load_classes()
        lessons = load_class_lessons()
        self.all_sidebar_rows = build_class_sidebar_rows(classes, lessons)
        self._refresh_visible()

    def toggle_class(self, key: str):
        if key in self.open_classes:
            self.open_classes = [k for k in self.open_classes if k != key]
        else:
            self.open_classes = [*self.open_classes, key]
        self._refresh_visible()

    def expand_class(self, key: str):
        if key not in self.open_classes:
            self.open_classes = [*self.open_classes, key]
            self._refresh_visible()

    def expand_path(self, path_key: str):
        if not path_key:
            return
        from HUST_Student.services.class_service import path_to_key, path_to_list

        parts = path_to_list(path_key)
        for i in range(len(parts)):
            partial = path_to_key(parts[: i + 1])
            name = parts[i]
            self.expand_class(f"{name}::{partial}")

    def set_active_path(self, path_key: str):
        self.current_path_key = path_key or ""
        parts = path_key.split("/") if path_key else []
        self.current_class = parts[-1] if parts else ""

    def collapse_all(self):
        self.open_classes = []
        self._refresh_visible()

    def select_class(self, name: str):
        self.current_class = name