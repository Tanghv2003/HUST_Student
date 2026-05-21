import json

from HUST_Student.core.paths import FOLDERS_JSON
from HUST_Student.services.studyset_service import (
    delete_studysets_under,
    rename_studyset_path_prefix,
)

PATH_SEP = "/"


def load_folders() -> dict:
    with open(FOLDERS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save_folders(data: dict) -> None:
    with open(FOLDERS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def path_to_list(path_key: str) -> list[str]:
    if not path_key:
        return []
    return path_key.split(PATH_SEP)


def path_to_key(path: list[str]) -> str:
    return PATH_SEP.join(path)


def normalize_node(node) -> dict:
    """Chuẩn hóa node folder — chỉ chứa folders (không có json)."""
    if not isinstance(node, dict):
        return {"folders": {}}
    if "folders" not in node:
        return {"folders": {}}
    return {"folders": node.get("folders", {})}


def get_parent_container(tree: dict, path: list[str]) -> dict | None:
    """Dict chứa key của folder đích (root tree nếu path 1 phần tử)."""
    if not path:
        return tree
    current = tree
    for name in path[:-1]:
        if name not in current:
            return None
        current = normalize_node(current[name])["folders"]
    return current


def get_folder_node(tree: dict, path: list[str]) -> dict | None:
    """Lấy node folder theo đường dẫn đầy đủ."""
    if not path:
        return None
    parent = get_parent_container(tree, path)
    if parent is None:
        return None
    name = path[-1]
    if name not in parent:
        return None
    return normalize_node(parent[name])


def find_folder_in_tree(tree: dict, path: list[str]) -> dict | None:
    """Dict các folder con trực tiếp của node tại path."""
    node = get_folder_node(tree, path)
    if node is None:
        return None
    return node["folders"]


def flatten_folder_tree(
    tree: dict,
    studysets: dict | None = None,
    parent_path: list[str] | None = None,
) -> list[dict]:
    """Duyệt đệ quy toàn bộ cây folder (bài giảng nằm trong studysets.json)."""
    parent_path = parent_path or []
    studysets = studysets or {}
    rows: list[dict] = []

    for name in sorted(tree.keys()):
        node = normalize_node(tree[name])
        path = [*parent_path, name]
        path_key = path_to_key(path)
        children = node.get("folders", {})
        set_count = len(studysets.get(path_key, []))
        child_count = len(children)

        level = len(path) - 1
        subtitle_parts = []
        if child_count > 0:
            subtitle_parts.append(f"{child_count} thư mục")
        if set_count > 0:
            subtitle_parts.append(f"{set_count} bài giảng")

        rows.append(
            {
                "name": name,
                "path_key": path_key,
                "level": level,
                "indent_px": f"{level * 18 + 8}px",
                "studyset_count": set_count,
                "child_folder_count": child_count,
                "subtitle": " · ".join(subtitle_parts),
                "has_children": child_count > 0 or set_count > 0,
            }
        )
        rows.extend(flatten_folder_tree(children, studysets, path))

    return rows


def rename_folder(old_path: list[str], new_name: str) -> bool:
    new_name = new_name.strip()
    if not old_path or not new_name:
        return False

    data = load_folders()
    parent = get_parent_container(data, old_path)
    if parent is None:
        return False

    old_name = old_path[-1]
    if old_name not in parent or new_name in parent:
        return False

    parent[new_name] = parent.pop(old_name)
    save_folders(data)

    old_key = path_to_key(old_path)
    new_key = path_to_key([*old_path[:-1], new_name])
    rename_studyset_path_prefix(old_key, new_key)
    return True


def delete_folder(folder_path: list[str]) -> bool:
    if not folder_path:
        return False

    data = load_folders()
    parent = get_parent_container(data, folder_path)
    if parent is None:
        return False

    name = folder_path[-1]
    if name not in parent:
        return False

    del parent[name]
    save_folders(data)
    delete_studysets_under(path_to_key(folder_path))
    return True


def add_subfolder(parent_path: list[str], subfolder_name: str) -> bool:
    name = subfolder_name.strip()
    if not name:
        return False

    data = load_folders()

    if parent_path:
        parent = find_folder_in_tree(data, parent_path)
        if parent is None:
            return False
    else:
        parent = data

    if name in parent:
        return False

    parent[name] = {"folders": {}}
    save_folders(data)
    return True


def build_sidebar_rows(
    tree: dict,
    studysets: dict,
    parent_path: list[str] | None = None,
    parent_tree_key: str = "",
) -> list[dict]:
    """Duyệt đệ quy folders + bài giảng cho sidebar."""
    parent_path = parent_path or []
    rows: list[dict] = []

    for name in sorted(tree.keys()):
        node = normalize_node(tree[name])
        path = [*parent_path, name]
        path_key = path_to_key(path)
        tree_key = f"{name}::{path_key}"
        children = node.get("folders", {})
        sets = studysets.get(path_key, [])
        level = len(path) - 1
        has_children = bool(children) or bool(sets)

        rows.append(
            {
                "row_type": "folder",
                "name": name,
                "path_key": path_key,
                "tree_key": tree_key,
                "level": level,
                "indent_px": f"{level * 14}px",
                "has_children": has_children,
                "parent_tree_key": parent_tree_key,
            }
        )

        for item in sets:
            rows.append(
                {
                    "row_type": "studyset",
                    "name": item.get("title", ""),
                    "title": item.get("title", ""),
                    "file": item.get("file", ""),
                    "terms": item.get("terms", 0),
                    "path_key": path_key,
                    "tree_key": f"set::{path_key}::{item.get('title', '')}",
                    "level": level + 1,
                    "indent_px": f"{(level + 1) * 14}px",
                    "parent_tree_key": tree_key,
                }
            )

        rows.extend(
            build_sidebar_rows(children, studysets, path, tree_key)
        )

    return rows


def get_folder_structure(folder_path: list[str] | None = None) -> dict:
    data = load_folders()
    if folder_path is None or not folder_path:
        return data
    node = get_folder_node(data, folder_path)
    return node if node else {}
