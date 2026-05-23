"""
class_manager_state.py — Quản lý lớp học + ghim lớp.
"""

import reflex as rx

from HUST_Student.services.class_service import (
    add_subclass,
    delete_class,
    flatten_class_tree,
    find_children_at_path,
    load_classes,
    path_to_key,
    path_to_list,
    rename_class,
    normalize_class_node,
)
from HUST_Student.services.class_lesson_service import (
    add_lesson,
    get_lessons_for_path,
    load_class_lessons_raw,
    remove_lesson,
)


class ClassManagerState(rx.State):

    selected_path_key: str = ""
    current_class_name: str = "Gốc"

    tree_rows: list[dict] = []
    class_lessons: list[dict] = []

    # ── Ghim lớp (runtime, không persist) ────────────────────────
    pinned_classes: list[dict] = []

    # ── Ghim bài giảng (runtime) ──────────────────────────────────
    pinned_lessons: list[dict] = []

    # ── Pinned tab navigation ─────────────────────────────────────
    # path đang xem trong tab ghim (có thể đi sâu vào sublclass)
    pinned_view_path: str = ""
    # dữ liệu subclasses của lớp đang xem trong tab ghim
    pinned_subclasses: list[dict] = []
    # bài giảng của lớp đang xem trong tab ghim
    pinned_view_lessons: list[dict] = []

    show_rename_dialog: bool = False
    show_add_subclass_dialog: bool = False
    show_delete_confirmation: bool = False
    show_add_lesson_dialog: bool = False

    new_class_name: str = ""
    new_subclass_name: str = ""
    new_lesson_title: str = ""
    new_lesson_file: str = ""

    message: str = ""
    message_type: str = ""

    # ── Computed ─────────────────────────────────────────────────

    @rx.var
    def is_at_root(self) -> bool:
        return self.selected_path_key == ""

    @rx.var
    def breadcrumb(self) -> str:
        if not self.selected_path_key:
            return "Gốc"
        return self.selected_path_key.replace("/", " › ")

    @rx.var
    def class_summary(self) -> str:
        if self.is_at_root:
            return "Thêm lớp gốc hoặc chọn lớp trong cây"
        n = len(self.class_lessons)
        return "Chưa có bài giảng nào" if n == 0 else f"{n} bài giảng"

    @rx.var
    def has_pinned_classes(self) -> bool:
        return len(self.pinned_classes) > 0

    @rx.var
    def pinned_class_keys(self) -> list[str]:
        return [p["pin_key"] for p in self.pinned_classes]

    # ── Pinned view computed ──────────────────────────────────────

    @rx.var
    def pinned_view_breadcrumb(self) -> str:
        if not self.pinned_view_path:
            return ""
        return self.pinned_view_path.replace("/", " › ")

    @rx.var
    def pinned_view_name(self) -> str:
        if not self.pinned_view_path:
            return ""
        parts = self.pinned_view_path.split("/")
        return parts[-1] if parts else ""

    @rx.var
    def pinned_view_parent_path(self) -> str:
        """Path cha để điều hướng back."""
        if not self.pinned_view_path:
            return ""
        parts = self.pinned_view_path.split("/")
        if len(parts) <= 1:
            return ""
        return "/".join(parts[:-1])

    @rx.var
    def pinned_view_can_go_back(self) -> bool:
        """Có thể back lên không (vẫn trong phạm vi lớp ghim)."""
        return bool(self.pinned_view_path) and "/" in self.pinned_view_path

    # ── Helpers ──────────────────────────────────────────────────

    async def _sync_sidebar(self):
        from HUST_Student.states.kanji_state import ClassTreeState
        tree = await self.get_state(ClassTreeState)
        tree.reload_class_tree()
        if self.selected_path_key:
            tree.expand_path(self.selected_path_key)
        tree.set_active_path(self.selected_path_key)

    def _rebuild_tree(self):
        data = load_classes()
        lessons = load_class_lessons_raw()
        rows = flatten_class_tree(data, lessons)
        pinned_keys = {p["pin_key"] for p in self.pinned_classes}
        for row in rows:
            row["is_pinned"] = row["path_key"] in pinned_keys
        self.tree_rows = rows

    def _load_lessons(self):
        if not self.selected_path_key:
            self.class_lessons = []
            return
        raw = get_lessons_for_path(self.selected_path_key)
        pinned_keys = {p["pin_key"] for p in self.pinned_lessons}
        self.class_lessons = [
            {
                "title": item.get("title", ""),
                "file": item.get("file", ""),
                "terms": item.get("terms", 0),
                "terms_label": f"{item.get('terms', 0)} mục",
                "pin_key": f"{self.selected_path_key}::{item.get('title', '')}",
                "is_pinned": f"{self.selected_path_key}::{item.get('title', '')}" in pinned_keys,
            }
            for item in raw
        ]

    def _reload_local(self):
        self._rebuild_tree()
        if self.selected_path_key:
            path = path_to_list(self.selected_path_key)
            self.current_class_name = path[-1] if path else "Gốc"
        else:
            self.current_class_name = "Gốc"
        self._load_lessons()

    def _set_message(self, msg: str, msg_type: str = "success"):
        self.message = msg
        self.message_type = msg_type

    def _class_display_path(self) -> str:
        if not self.selected_path_key:
            return "Gốc"
        return self.selected_path_key.replace("/", " › ")

    def _load_pinned_view(self, path_key: str):
        """Load subclasses + lessons cho pinned tab view tại path_key."""
        self.pinned_view_path = path_key
        if not path_key:
            self.pinned_subclasses = []
            self.pinned_view_lessons = []
            return

        # Load subclasses
        data = load_classes()
        path = path_to_list(path_key)
        children = find_children_at_path(data, path) or {}
        lessons_raw = load_class_lessons_raw()

        subclasses = []
        for name in sorted(children.keys()):
            node = normalize_class_node(children[name])
            child_path = f"{path_key}/{name}"
            child_children = node.get("classes", {})
            lesson_count = len(lessons_raw.get(child_path, []))
            child_count = len(child_children)

            subtitle_parts = []
            if child_count:
                subtitle_parts.append(f"{child_count} lớp con")
            if lesson_count:
                subtitle_parts.append(f"{lesson_count} bài giảng")

            subclasses.append({
                "name": name,
                "path_key": child_path,
                "icon": node.get("icon", "graduation-cap"),
                "color": node.get("color", "#4257B2"),
                "students": node.get("students", 0),
                "subtitle": " · ".join(subtitle_parts) if subtitle_parts else "Lớp trống",
                "has_children": bool(child_count or lesson_count),
            })
        self.pinned_subclasses = subclasses

        # Load lessons at current path
        raw_lessons = get_lessons_for_path(path_key)
        self.pinned_view_lessons = [
            {
                "title": item.get("title", ""),
                "file": item.get("file", ""),
                "terms": item.get("terms", 0),
                "terms_label": f"{item.get('terms', 0)} mục",
            }
            for item in raw_lessons
        ]

    # ── Selection ────────────────────────────────────────────────

    @rx.event
    async def load_current_class(self, class_path: list[str] | None = None):
        if class_path:
            self.selected_path_key = path_to_key(class_path)
        else:
            self.selected_path_key = ""
        self._reload_local()
        await self._sync_sidebar()

    def apply_selection(self, path_key: str):
        self.selected_path_key = str(path_key) if path_key else ""
        self._reload_local()

    @rx.event
    async def select_class(self, path_key: str):
        self.apply_selection(path_key)
        await self._sync_sidebar()

    # ── Pinned tab navigation ─────────────────────────────────────

    def open_pinned_class(self, path_key: str):
        """Mở tab ghim và load view tại path_key của lớp ghim."""
        self._load_pinned_view(path_key)

    def navigate_pinned_into(self, path_key: str):
        """Đi sâu vào subclass trong tab ghim."""
        self._load_pinned_view(path_key)

    def navigate_pinned_back(self):
        """Quay lại lớp cha trong tab ghim."""
        parent = self.pinned_view_parent_path
        self._load_pinned_view(parent)

    def navigate_pinned_to(self, path_key: str):
        """Điều hướng tới bất kỳ path nào trong tab ghim (dùng cho breadcrumb)."""
        self._load_pinned_view(path_key)

    # ── Pin / Unpin lớp ──────────────────────────────────────────

    def toggle_pin_class(self, path_key: str):
        pin_key = path_key
        existing = [p for p in self.pinned_classes if p["pin_key"] == pin_key]
        if existing:
            self.pinned_classes = [p for p in self.pinned_classes if p["pin_key"] != pin_key]
        else:
            name = path_key.split("/")[-1] if path_key else path_key
            for row in self.tree_rows:
                if row["path_key"] == path_key:
                    name = row["name"]
                    break
            self.pinned_classes = list(self.pinned_classes) + [
                {
                    "name": name,
                    "path_key": path_key,
                    "pin_key": pin_key,
                    "breadcrumb": path_key.replace("/", " › "),
                }
            ]
        self._rebuild_tree()

    def unpin_class(self, pin_key: str):
        self.pinned_classes = [p for p in self.pinned_classes if p["pin_key"] != pin_key]
        self._rebuild_tree()

    def clear_all_pinned_classes(self):
        self.pinned_classes = []
        self._rebuild_tree()

    # ── Pin / Unpin bài giảng ─────────────────────────────────────

    def toggle_pin_lesson(self, pin_key: str):
        existing = [p for p in self.pinned_lessons if p["pin_key"] == pin_key]
        if existing:
            self.pinned_lessons = [p for p in self.pinned_lessons if p["pin_key"] != pin_key]
        else:
            lesson = next((l for l in self.class_lessons if l["pin_key"] == pin_key), None)
            if lesson:
                self.pinned_lessons = list(self.pinned_lessons) + [
                    {
                        "title": lesson["title"],
                        "file": lesson["file"],
                        "terms_label": lesson["terms_label"],
                        "path_key": self.selected_path_key,
                        "class_path": self._class_display_path(),
                        "pin_key": pin_key,
                    }
                ]
        self._refresh_pin_flags()

    def unpin_lesson(self, pin_key: str):
        self.pinned_lessons = [p for p in self.pinned_lessons if p["pin_key"] != pin_key]
        self._refresh_pin_flags()

    def _refresh_pin_flags(self):
        pinned_keys = {p["pin_key"] for p in self.pinned_lessons}
        self.class_lessons = [
            {**l, "is_pinned": l["pin_key"] in pinned_keys}
            for l in self.class_lessons
        ]

    def clear_all_pins(self):
        self.pinned_lessons = []
        self._refresh_pin_flags()

    # ── Add subclass ──────────────────────────────────────────────

    def open_add_subclass_dialog(self):
        self.new_subclass_name = ""
        self.show_add_subclass_dialog = True
        self.message = ""

    def close_add_subclass_dialog(self):
        self.show_add_subclass_dialog = False
        self.new_subclass_name = ""

    def set_new_subclass_name(self, value: str):
        self.new_subclass_name = str(value) if value else ""

    @rx.event
    async def confirm_add_subclass(self):
        name = self.new_subclass_name.strip()
        if not name:
            self._set_message("❌ Tên lớp không được để trống.", "error")
            return
        if add_subclass(path_to_list(self.selected_path_key), name):
            self._set_message(f"✅ Đã thêm lớp '{name}'")
            self.close_add_subclass_dialog()
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message(f"❌ Lớp '{name}' đã tồn tại hoặc có lỗi.", "error")

    # ── Rename class ──────────────────────────────────────────────

    def open_rename_dialog(self):
        if self.is_at_root:
            self._set_message("❌ Chọn một lớp để đổi tên.", "error")
            return
        self.new_class_name = self.current_class_name
        self.show_rename_dialog = True
        self.message = ""

    def close_rename_dialog(self):
        self.show_rename_dialog = False
        self.new_class_name = ""

    def set_new_class_name(self, value: str):
        self.new_class_name = str(value) if value else ""

    @rx.event
    async def confirm_rename_class(self):
        if self.is_at_root:
            self._set_message("❌ Không thể đổi tên thư mục gốc.", "error")
            return
        path = path_to_list(self.selected_path_key)
        new_name = self.new_class_name.strip()
        if not new_name:
            self._set_message("❌ Tên mới không được để trống.", "error")
            return
        if new_name == path[-1]:
            self.close_rename_dialog()
            return
        if rename_class(path, new_name):
            old_key = self.selected_path_key
            new_key = path_to_key([*path[:-1], new_name])
            self.selected_path_key = new_key
            self.pinned_classes = [
                {**p,
                 "path_key": p["path_key"].replace(old_key, new_key, 1),
                 "pin_key": p["pin_key"].replace(old_key, new_key, 1),
                 "breadcrumb": p["breadcrumb"].replace(path[-1], new_name, 1),
                } if p["path_key"].startswith(old_key) else p
                for p in self.pinned_classes
            ]
            self.pinned_lessons = [
                {**p,
                 "path_key": p["path_key"].replace(old_key, new_key, 1),
                 "class_path": p["class_path"].replace(path[-1], new_name, 1),
                 "pin_key": p["pin_key"].replace(old_key, new_key, 1),
                } if p["path_key"].startswith(old_key) else p
                for p in self.pinned_lessons
            ]
            self._set_message(f"✅ Đã đổi tên thành '{new_name}'")
            self.close_rename_dialog()
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message("❌ Lỗi đổi tên (có thể trùng tên).", "error")

    # ── Delete class ──────────────────────────────────────────────

    def open_delete_confirmation(self):
        if self.is_at_root:
            self._set_message("❌ Chọn một lớp để xoá.", "error")
            return
        self.show_delete_confirmation = True
        self.message = ""

    def close_delete_confirmation(self):
        self.show_delete_confirmation = False

    @rx.event
    async def confirm_delete_class(self):
        if self.is_at_root:
            self._set_message("❌ Không thể xoá thư mục gốc.", "error")
            self.close_delete_confirmation()
            return
        path = path_to_list(self.selected_path_key)
        parent_key = path_to_key(path[:-1])
        deleted_key = self.selected_path_key
        if delete_class(path):
            self.pinned_classes = [
                p for p in self.pinned_classes
                if not p["path_key"].startswith(deleted_key)
            ]
            self.pinned_lessons = [
                p for p in self.pinned_lessons
                if not p["path_key"].startswith(deleted_key)
            ]
            self._set_message(f"✅ Đã xoá lớp '{path[-1]}'")
            self.close_delete_confirmation()
            self.selected_path_key = parent_key
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message("❌ Lỗi khi xoá lớp.", "error")
            self.close_delete_confirmation()

    # ── Add lesson ────────────────────────────────────────────────

    def open_add_lesson_dialog(self):
        if self.is_at_root:
            self._set_message("❌ Chọn một lớp để thêm bài giảng.", "error")
            return
        self.new_lesson_title = ""
        self.new_lesson_file = ""
        self.show_add_lesson_dialog = True
        self.message = ""

    def close_add_lesson_dialog(self):
        self.show_add_lesson_dialog = False
        self.new_lesson_title = ""
        self.new_lesson_file = ""

    def set_new_lesson_title(self, value: str):
        self.new_lesson_title = str(value) if value else ""

    def set_new_lesson_file(self, value: str):
        self.new_lesson_file = str(value) if value else ""

    @rx.event
    async def confirm_add_lesson(self):
        if self.is_at_root:
            self._set_message("❌ Chọn lớp để thêm bài giảng.", "error")
            return
        title = self.new_lesson_title.strip()
        file_path = self.new_lesson_file.strip()
        if not title:
            self._set_message("❌ Tên bài giảng không được để trống.", "error")
            return
        if not file_path:
            self._set_message("❌ Đường dẫn file không được để trống.", "error")
            return
        if add_lesson(self.selected_path_key, title, file_path):
            self._set_message(f"✅ Đã thêm bài giảng '{title}'")
            self.close_add_lesson_dialog()
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message(f"❌ Bài giảng '{title}' đã tồn tại hoặc có lỗi.", "error")

    # ── Remove lesson ─────────────────────────────────────────────

    @rx.event
    async def remove_lesson_item(self, title: str):
        if not self.selected_path_key:
            return
        pin_key = f"{self.selected_path_key}::{title}"
        self.pinned_lessons = [p for p in self.pinned_lessons if p["pin_key"] != pin_key]
        if remove_lesson(self.selected_path_key, title):
            self._set_message(f"✅ Đã xoá bài giảng '{title}'")
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message("❌ Lỗi khi xoá bài giảng.", "error")

    def clear_message(self):
        self.message = ""
        self.message_type = ""