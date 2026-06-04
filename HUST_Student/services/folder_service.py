"""
folder_service.py — Toàn bộ nghiệp vụ CRUD cho folder tree.

Cấu trúc folders.json:
{
  "TênFolder": {
    "folders": {
      "TênFolderCon": { "folders": {} }
    }
  }
}

Bài giảng (studysets) được lưu riêng trong studysets.json với key = path_key.

THAY ĐỔI: add_subfolder nay tự tạo thư mục vật lý trong data/studysets/<path>/
"""

import json
from pathlib import Path

from HUST_Student.core.paths import FOLDERS_JSON, STUDYSETS_DIR
from HUST_Student.services.studyset_service import (
    delete_studysets_under,
    rename_studyset_path_prefix,
)

PATH_SEP = "/"


# ══════════════════════════════════════════════════════════════════
# I/O
# ══════════════════════════════════════════════════════════════════

def load_folders() -> dict:
    try:
        with open(FOLDERS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_folders(data: dict) -> None:
    with open(FOLDERS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════════
# PATH HELPERS
# ══════════════════════════════════════════════════════════════════

def path_to_list(path_key: str) -> list[str]:
    if not path_key:
        return []
    return [p for p in path_key.split(PATH_SEP) if p]


def path_to_key(path: list[str]) -> str:
    return PATH_SEP.join(p for p in path if p)


def normalize_node(node) -> dict:
    """Chuẩn hoá một node: đảm bảo luôn có key 'folders'."""
    if not isinstance(node, dict):
        return {"folders": {}}
    folders = node.get("folders")
    if not isinstance(folders, dict):
        folders = {}
    return {"folders": folders}


# ══════════════════════════════════════════════════════════════════
# PHYSICAL FOLDER HELPERS
# ══════════════════════════════════════════════════════════════════

def _physical_folder_path(path_key: str) -> Path:
    """Trả về đường dẫn vật lý tương ứng trong data/studysets/."""
    parts = path_to_list(path_key)
    return STUDYSETS_DIR.joinpath(*parts) if parts else STUDYSETS_DIR


def _create_physical_folder(path_key: str) -> None:
    """Tạo thư mục vật lý trong data/studysets/<path_key>/."""
    folder = _physical_folder_path(path_key)
    folder.mkdir(parents=True, exist_ok=True)


def _rename_physical_folder(old_path_key: str, new_path_key: str) -> None:
    """Đổi tên / di chuyển thư mục vật lý nếu tồn tại."""
    old = _physical_folder_path(old_path_key)
    new = _physical_folder_path(new_path_key)
    if old.exists() and not new.exists():
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)


def _delete_physical_folder(path_key: str) -> None:
    """Xoá thư mục vật lý và toàn bộ nội dung bên trong."""
    import shutil
    folder = _physical_folder_path(path_key)
    if folder.exists():
        shutil.rmtree(folder, ignore_errors=True)


# ══════════════════════════════════════════════════════════════════
# TREE NAVIGATION
# ══════════════════════════════════════════════════════════════════

def _get_subtree(tree: dict, path: list[str]) -> dict | None:
    """
    Trả về dict 'folders' của node tại path.
    path=[] → trả về tree gốc.
    """
    if not path:
        return tree
    current = tree
    for name in path:
        if name not in current:
            return None
        current = normalize_node(current[name])["folders"]
    return current


def get_parent_container(tree: dict, path: list[str]) -> dict | None:
    """
    Trả về dict chứa key của folder đích
    (tức là subtree của parent, hoặc tree gốc nếu path có 1 phần tử).
    """
    if not path:
        return None
    return _get_subtree(tree, path[:-1])


def get_folder_node(tree: dict, path: list[str]) -> dict | None:
    """Trả về node (đã normalize) của folder tại path."""
    if not path:
        return None
    parent = get_parent_container(tree, path)
    if parent is None or path[-1] not in parent:
        return None
    return normalize_node(parent[path[-1]])


def find_folder_in_tree(tree: dict, path: list[str]) -> dict | None:
    """Trả về dict children của node tại path."""
    node = get_folder_node(tree, path)
    return node["folders"] if node else None


# ══════════════════════════════════════════════════════════════════
# FLATTEN (dùng cho FolderManagerState tree_rows)
# ══════════════════════════════════════════════════════════════════

def flatten_folder_tree(
    tree: dict,
    studysets: dict | None = None,
    parent_path: list[str] | None = None,
) -> list[dict]:
    """Duyệt đệ quy toàn bộ cây folder, trả về danh sách flat rows."""
    parent_path = parent_path or []
    studysets = studysets or {}
    rows: list[dict] = []

    for name in sorted(tree.keys()):
        node = normalize_node(tree[name])
        path = [*parent_path, name]
        path_key = path_to_key(path)
        children = node["folders"]
        set_count = len(studysets.get(path_key, []))
        child_count = len(children)
        level = len(path) - 1

        subtitle_parts = []
        if child_count:
            subtitle_parts.append(f"{child_count} thư mục con")
        if set_count:
            subtitle_parts.append(f"{set_count} bài giảng")

        rows.append({
            "name": name,
            "path_key": path_key,
            "level": level,
            "indent_px": f"{level * 18 + 8}px",
            "studyset_count": set_count,
            "child_folder_count": child_count,
            "subtitle": " · ".join(subtitle_parts) if subtitle_parts else "Thư mục trống",
            "has_children": bool(child_count or set_count),
        })
        rows.extend(flatten_folder_tree(children, studysets, path))

    return rows


# ══════════════════════════════════════════════════════════════════
# SIDEBAR ROWS (dùng cho TreeState)
# ══════════════════════════════════════════════════════════════════

def build_sidebar_rows(
    tree: dict,
    studysets: dict,
    parent_path: list[str] | None = None,
    parent_tree_key: str = "",
) -> list[dict]:
    """
    Duyệt đệ quy folder + bài giảng, tạo danh sách row cho sidebar.
    Mỗi row có row_type = "folder" | "studyset".
    """
    parent_path = parent_path or []
    rows: list[dict] = []

    for name in sorted(tree.keys()):
        node = normalize_node(tree[name])
        path = [*parent_path, name]
        path_key = path_to_key(path)
        tree_key = f"{name}::{path_key}"
        children = node["folders"]
        sets = studysets.get(path_key, [])
        level = len(path) - 1

        rows.append({
            "row_type": "folder",
            "name": name,
            "path_key": path_key,
            "tree_key": tree_key,
            "level": level,
            "indent_px": f"{level * 14}px",
            "has_children": bool(children) or bool(sets),
            "parent_tree_key": parent_tree_key,
        })

        for item in sets:
            rows.append({
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
            })

        rows.extend(build_sidebar_rows(children, studysets, path, tree_key))

    return rows


# ══════════════════════════════════════════════════════════════════
# CRUD OPERATIONS
# ══════════════════════════════════════════════════════════════════

def add_subfolder(parent_path: list[str], subfolder_name: str) -> tuple[bool, str]:
    """
    Thêm folder con vào parent_path.
    parent_path=[] → thêm vào gốc.
    Đồng thời tạo thư mục vật lý tương ứng trong data/studysets/.
    Trả về (success, error_message).
    """
    name = subfolder_name.strip()
    if not name:
        return False, "Tên thư mục không được để trống."

    data = load_folders()

    if parent_path:
        parent = _get_subtree(data, parent_path)
        if parent is None:
            return False, f"Không tìm thấy thư mục cha: {path_to_key(parent_path)}"
    else:
        parent = data

    if name in parent:
        return False, f"Thư mục '{name}' đã tồn tại."

    parent[name] = {"folders": {}}
    save_folders(data)

    # Tạo thư mục vật lý
    new_path_key = path_to_key([*parent_path, name])
    _create_physical_folder(new_path_key)

    return True, ""


def rename_folder(old_path: list[str], new_name: str) -> tuple[bool, str]:
    """
    Đổi tên folder tại old_path thành new_name.
    Cũng đổi prefix tương ứng trong studysets.json và thư mục vật lý.
    """
    new_name = new_name.strip()
    if not old_path:
        return False, "Không thể đổi tên thư mục gốc."
    if not new_name:
        return False, "Tên mới không được để trống."

    data = load_folders()
    parent = get_parent_container(data, old_path)
    if parent is None:
        return False, "Không tìm thấy thư mục cha."

    old_name = old_path[-1]
    if old_name not in parent:
        return False, f"Không tìm thấy thư mục '{old_name}'."
    if new_name != old_name and new_name in parent:
        return False, f"Thư mục '{new_name}' đã tồn tại."

    if new_name != old_name:
        parent[new_name] = parent.pop(old_name)
        save_folders(data)
        old_key = path_to_key(old_path)
        new_key = path_to_key([*old_path[:-1], new_name])
        rename_studyset_path_prefix(old_key, new_key)
        # Đổi tên thư mục vật lý
        _rename_physical_folder(old_key, new_key)

    return True, ""


def delete_folder(folder_path: list[str]) -> tuple[bool, str]:
    """
    Xoá folder và toàn bộ folder con + bài giảng bên trong.
    Đồng thời xoá thư mục vật lý tương ứng.
    """
    if not folder_path:
        return False, "Không thể xoá thư mục gốc."

    data = load_folders()
    parent = get_parent_container(data, folder_path)
    if parent is None:
        return False, "Không tìm thấy thư mục cha."

    name = folder_path[-1]
    if name not in parent:
        return False, f"Không tìm thấy thư mục '{name}'."

    del parent[name]
    save_folders(data)

    path_key = path_to_key(folder_path)
    delete_studysets_under(path_key)
    # Xoá thư mục vật lý
    _delete_physical_folder(path_key)

    return True, ""


def move_folder(src_path: list[str], dst_parent_path: list[str]) -> tuple[bool, str]:
    """
    Di chuyển folder từ src_path sang dst_parent_path.
    Không thể di chuyển folder vào chính nó hoặc con của nó.
    """
    if not src_path:
        return False, "Không thể di chuyển thư mục gốc."

    src_key = path_to_key(src_path)
    dst_key = path_to_key(dst_parent_path)

    if dst_key == src_key or dst_key.startswith(src_key + PATH_SEP):
        return False, "Không thể di chuyển thư mục vào chính nó hoặc thư mục con của nó."

    data = load_folders()

    src_parent = get_parent_container(data, src_path)
    if src_parent is None or src_path[-1] not in src_parent:
        return False, "Không tìm thấy thư mục nguồn."

    if dst_parent_path:
        dst_parent = _get_subtree(data, dst_parent_path)
        if dst_parent is None:
            return False, "Không tìm thấy thư mục đích."
    else:
        dst_parent = data

    folder_name = src_path[-1]
    if folder_name in dst_parent:
        return False, f"Thư mục '{folder_name}' đã tồn tại tại đích."

    node = src_parent.pop(folder_name)
    dst_parent[folder_name] = node
    save_folders(data)

    new_path = [*dst_parent_path, folder_name]
    new_key = path_to_key(new_path)
    rename_studyset_path_prefix(src_key, new_key)
    # Di chuyển thư mục vật lý
    _rename_physical_folder(src_key, new_key)

    return True, ""


def get_folder_structure(folder_path: list[str] | None = None) -> dict:
    data = load_folders()
    if not folder_path:
        return data
    node = get_folder_node(data, folder_path)
    return node if node else {}


def folder_exists(path: list[str]) -> bool:
    data = load_folders()
    return get_folder_node(data, path) is not None


def get_all_folder_paths(tree: dict | None = None, parent_path: list[str] | None = None) -> list[str]:
    """Trả về danh sách tất cả path_key của mọi folder trong cây."""
    if tree is None:
        tree = load_folders()
    parent_path = parent_path or []
    paths: list[str] = []
    for name, node in tree.items():
        path = [*parent_path, name]
        paths.append(path_to_key(path))
        node = normalize_node(node)
        paths.extend(get_all_folder_paths(node["folders"], path))
    return paths