"""
studyset_service.py — CRUD bài giảng trong studysets.json.

Mỗi entry trong studysets.json:
  "path_key": [{"title": "...", "file": "...", "terms": N}]

THAY ĐỔI:
  - add_studyset giờ tự sinh đường dẫn file từ title + path_key
  - Tự tạo file JSON rỗng [] trong thư mục tương ứng
  - Không cần truyền file_path từ ngoài vào
"""

import json
import re
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


def load_studyset_raw_text(file_path: str) -> str:
    resolved = STUDYSETS_DIR / Path(file_path)
    with open(resolved, "r", encoding="utf-8") as f:
        return f.read()


def save_studyset_raw_text(file_path: str, text: str) -> None:
    resolved = STUDYSETS_DIR / Path(file_path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    with open(resolved, "w", encoding="utf-8") as f:
        f.write(text)


def save_studyset_detail(file_path: str, words_list: list[dict]) -> None:
    resolved = STUDYSETS_DIR / Path(file_path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    with open(resolved, "w", encoding="utf-8") as f:
        json.dump(words_list, f, ensure_ascii=False, indent=2)


def detect_keys_from_file(file_path: str) -> tuple[str, str]:
    resolved = STUDYSETS_DIR / Path(file_path)
    try:
        with open(resolved, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                first = data[0]
                front_key = "foreign" if "foreign" in first else ("vietnamese" if "vietnamese" in first else "front")
                back_key = "native" if "native" in first else ("japanese" if "japanese" in first else "back")
                return front_key, back_key
    except Exception:
        pass
    return "foreign", "native"


def save_studyset_words(file_path: str, words: list) -> None:
    front_key, back_key = detect_keys_from_file(file_path)
    raw_data = []
    for w in words:
        raw_data.append({
            front_key: w.front,
            back_key: w.back
        })
    save_studyset_detail(file_path, raw_data)


# ══════════════════════════════════════════════════════════════════
# AUTO FILE PATH GENERATION
# ══════════════════════════════════════════════════════════════════

def _slugify(text: str) -> str:
    """
    Chuyển tiêu đề thành tên file an toàn:
    - Giữ lại chữ cái, số, dấu gạch ngang, gạch dưới
    - Thay khoảng trắng bằng gạch dưới
    - Loại bỏ ký tự đặc biệt không hợp lệ
    """
    # Thay khoảng trắng và dấu chấm câu thông dụng bằng _
    text = re.sub(r"[\s\-–—]+", "_", text.strip())
    # Giữ chữ cái Unicode (bao gồm tiếng Việt/Nhật), số, _, .
    text = re.sub(r"[^\w.]", "", text, flags=re.UNICODE)
    # Bỏ dấu _ hoặc . ở đầu/cuối
    text = text.strip("_.")
    return text or "studyset"


def _build_file_path(path_key: str, title: str) -> str:
    """
    Sinh đường dẫn file tương đối trong data/studysets/.
    Ví dụ: path_key="Tiếng Nhật/DAICHI/Bài 21", title="Từ vựng mới"
    → "Tiếng_Nhật/DAICHI/Bài_21/Từ_vựng_mới.json"
    """
    # Chuyển từng phần của path_key thành tên thư mục an toàn
    parts = [p for p in path_key.split("/") if p]
    safe_parts = [_slugify(p) for p in parts]

    # Tên file từ title
    safe_title = _slugify(title)

    if safe_parts:
        return "/".join(safe_parts) + f"/{safe_title}.json"
    else:
        return f"{safe_title}.json"


def _ensure_unique_file_path(base_path: str) -> str:
    """
    Nếu file đã tồn tại, thêm hậu tố _2, _3, ... cho đến khi tìm được tên chưa dùng.
    """
    resolved = STUDYSETS_DIR / Path(base_path)
    if not resolved.exists():
        return base_path

    stem = Path(base_path).stem
    suffix = Path(base_path).suffix
    parent = str(Path(base_path).parent)

    counter = 2
    while True:
        candidate = f"{parent}/{stem}_{counter}{suffix}"
        if not (STUDYSETS_DIR / Path(candidate)).exists():
            return candidate
        counter += 1


def create_empty_studyset_file(file_path: str) -> None:
    """Tạo file JSON rỗng [] tại đường dẫn đã cho."""
    resolved = STUDYSETS_DIR / Path(file_path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    with open(resolved, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)


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

def add_studyset(path_key: str, title: str, file_path: str = "") -> tuple[bool, str]:
    """
    Thêm bài giảng vào path_key.

    Nếu file_path để trống, tự động sinh từ path_key + title và tạo file JSON rỗng.
    Trả về (success, error_message).
    """
    title = title.strip()
    if not path_key:
        return False, "path_key không được để trống."
    if not title:
        return False, "Tên bài giảng không được để trống."

    data = load_studysets_raw()
    sets = data.setdefault(path_key, [])

    if any(s.get("title") == title for s in sets):
        return False, f"Bài giảng '{title}' đã tồn tại."

    # Tự sinh đường dẫn nếu không được truyền vào
    if not file_path or not file_path.strip():
        auto_path = _build_file_path(path_key, title)
        file_path = _ensure_unique_file_path(auto_path)
        # Tạo file JSON rỗng
        try:
            create_empty_studyset_file(file_path)
        except Exception as e:
            return False, f"Không thể tạo file: {e}"
    else:
        file_path = file_path.strip()

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
    data[src_path] = [s for s in src_sets if s.get("title") != title]
    if not data[src_path]:
        del data[src_path]
    dst_sets.append(item)
    data[dst_path] = dst_sets
    save_studysets(data)
    return True, ""