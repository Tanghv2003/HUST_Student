import json

from HUST_Student.core.paths import CLASSES_JSON
from HUST_Student.services.class_lesson_service import (
    delete_lessons_under,
    rename_lesson_path_prefix,
)

PATH_SEP = "/"
CHILDREN_KEY = "classes"
DEFAULT_NODE = {
    "icon": "graduation-cap",
    "color": "#4257B2",
    "students": 0,
    "classes": {},
}


def load_classes() -> dict:
    with open(CLASSES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save_classes(data: dict) -> None:
    with open(CLASSES_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def path_to_list(path_key: str) -> list[str]:
    if not path_key:
        return []
    return path_key.split(PATH_SEP)


def path_to_key(path: list[str]) -> str:
    return PATH_SEP.join(path)


def normalize_class_node(node) -> dict:
    if not isinstance(node, dict):
        return dict(DEFAULT_NODE)
    return {
        "icon": node.get("icon", DEFAULT_NODE["icon"]),
        "color": node.get("color", DEFAULT_NODE["color"]),
        "students": node.get("students", 0),
        "classes": node.get("classes", {}),
    }


def get_parent_container(tree: dict, path: list[str]) -> dict | None:
    if not path:
        return tree
    current = tree
    for name in path[:-1]:
        if name not in current:
            return None
        current = normalize_class_node(current[name])[CHILDREN_KEY]
    return current


def get_class_node(tree: dict, path: list[str]) -> dict | None:
    if not path:
        return None
    parent = get_parent_container(tree, path)
    if parent is None:
        return None
    name = path[-1]
    if name not in parent:
        return None
    return normalize_class_node(parent[name])


def find_children_at_path(tree: dict, path: list[str]) -> dict | None:
    node = get_class_node(tree, path)
    if node is None:
        return None
    return node[CHILDREN_KEY]


def flatten_class_tree(
    tree: dict,
    lessons: dict | None = None,
    parent_path: list[str] | None = None,
) -> list[dict]:
    parent_path = parent_path or []
    lessons = lessons or {}
    rows: list[dict] = []

    for name in sorted(tree.keys()):
        node = normalize_class_node(tree[name])
        path = [*parent_path, name]
        path_key = path_to_key(path)
        children = node[CHILDREN_KEY]
        lesson_count = len(lessons.get(path_key, []))
        child_count = len(children)
        level = len(path) - 1

        subtitle_parts = []
        if child_count > 0:
            subtitle_parts.append(f"{child_count} lớp con")
        if lesson_count > 0:
            subtitle_parts.append(f"{lesson_count} bài giảng")

        rows.append(
            {
                "name": name,
                "path_key": path_key,
                "level": level,
                "indent_px": f"{level * 18 + 8}px",
                "icon": node["icon"],
                "color": node["color"],
                "students": node["students"],
                "lesson_count": lesson_count,
                "child_count": child_count,
                "subtitle": " · ".join(subtitle_parts),
                "has_children": child_count > 0 or lesson_count > 0,
            }
        )
        rows.extend(flatten_class_tree(children, lessons, path))

    return rows


def build_class_sidebar_rows(
    tree: dict,
    lessons: dict,
    parent_path: list[str] | None = None,
    parent_tree_key: str = "",
) -> list[dict]:
    parent_path = parent_path or []
    rows: list[dict] = []

    for name in sorted(tree.keys()):
        node = normalize_class_node(tree[name])
        path = [*parent_path, name]
        path_key = path_to_key(path)
        tree_key = f"{name}::{path_key}"
        children = node[CHILDREN_KEY]
        class_lessons = lessons.get(path_key, [])
        level = len(path) - 1
        has_children = bool(children) or bool(class_lessons)

        rows.append(
            {
                "row_type": "class",
                "name": name,
                "path_key": path_key,
                "tree_key": tree_key,
                "level": level,
                "indent_px": f"{level * 14}px",
                "icon": node["icon"],
                "color": node["color"],
                "students": node["students"],
                "has_children": has_children,
                "parent_tree_key": parent_tree_key,
            }
        )

        for item in class_lessons:
            rows.append(
                {
                    "row_type": "lesson",
                    "name": item.get("title", ""),
                    "title": item.get("title", ""),
                    "file": item.get("file", ""),
                    "terms": item.get("terms", 0),
                    "path_key": path_key,
                    "tree_key": f"lesson::{path_key}::{item.get('title', '')}",
                    "level": level + 1,
                    "indent_px": f"{(level + 1) * 14}px",
                    "parent_tree_key": tree_key,
                }
            )

        rows.extend(build_class_sidebar_rows(children, lessons, path, tree_key))

    return rows


def rename_class(old_path: list[str], new_name: str) -> bool:
    new_name = new_name.strip()
    if not old_path or not new_name:
        return False

    data = load_classes()
    parent = get_parent_container(data, old_path)
    if parent is None:
        return False

    old_name = old_path[-1]
    if old_name not in parent or new_name in parent:
        return False

    parent[new_name] = parent.pop(old_name)
    save_classes(data)

    old_key = path_to_key(old_path)
    new_key = path_to_key([*old_path[:-1], new_name])
    rename_lesson_path_prefix(old_key, new_key)
    return True


def delete_class(class_path: list[str]) -> bool:
    if not class_path:
        return False

    data = load_classes()
    parent = get_parent_container(data, class_path)
    if parent is None:
        return False

    name = class_path[-1]
    if name not in parent:
        return False

    del parent[name]
    save_classes(data)
    delete_lessons_under(path_to_key(class_path))
    return True


def add_subclass(parent_path: list[str], subclass_name: str) -> bool:
    name = subclass_name.strip()
    if not name:
        return False

    data = load_classes()

    if parent_path:
        parent = find_children_at_path(data, parent_path)
        if parent is None:
            return False
    else:
        parent = data

    if name in parent:
        return False

    parent[name] = dict(DEFAULT_NODE)
    save_classes(data)
    return True
