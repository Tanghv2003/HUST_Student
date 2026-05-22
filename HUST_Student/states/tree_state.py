"""
tree_state.py — Cây thư mục sidebar, reactive với folders.json & studysets.json.

Luồng:
  1. reload_sidebar() đọc lại toàn bộ dữ liệu, tạo all_sidebar_rows
  2. _refresh_visible() lọc visible_sidebar_rows theo open_folders
  3. toggle_folder / expand_folder / expand_path điều khiển trạng thái mở/đóng
"""

import reflex as rx

from HUST_Student.services.folder_service import (
    build_sidebar_rows,
    load_folders,
    path_to_key,
    path_to_list,
)
from HUST_Student.services.studyset_service import load_studysets


class TreeState(rx.State):
    """Cây thư mục sidebar."""

    open_folders: list[str] = []
    all_sidebar_rows: list[dict] = []
    visible_sidebar_rows: list[dict] = []

    # ── Internal ─────────────────────────────────────────────────

    def _refresh_visible(self):
        """Cập nhật visible_sidebar_rows theo open_folders hiện tại."""
        open_set = set(self.open_folders)
        visible = []
        for row in self.all_sidebar_rows:
            if row["level"] == 0:
                visible.append(row)
            elif row.get("parent_tree_key", "") in open_set:
                visible.append(row)
        self.visible_sidebar_rows = visible

    # ── Public actions ────────────────────────────────────────────

    def reload_sidebar(self):
        """
        Đọc lại toàn bộ folders.json + studysets.json và rebuild rows.
        Gọi sau mọi thao tác CRUD.
        """
        folders = load_folders()
        studysets = load_studysets()
        self.all_sidebar_rows = build_sidebar_rows(folders, studysets)
        self._refresh_visible()

    def toggle_folder(self, key: str):
        """Mở/đóng folder theo tree_key."""
        if key in self.open_folders:
            # Đóng folder này VÀ toàn bộ con của nó
            self.open_folders = [
                k for k in self.open_folders
                if k != key and not k.startswith(key + "::")
            ]
        else:
            self.open_folders = [*self.open_folders, key]
        self._refresh_visible()

    def expand_folder(self, key: str):
        """Mở folder nếu chưa mở."""
        if key not in self.open_folders:
            self.open_folders = [*self.open_folders, key]
            self._refresh_visible()

    def collapse_folder(self, key: str):
        """Đóng folder và con."""
        self.open_folders = [
            k for k in self.open_folders
            if k != key and not k.startswith(key + "::")
        ]
        self._refresh_visible()

    def expand_path(self, path_key: str):
        """
        Mở tất cả folder cha trên đường tới path_key.
        Dùng sau khi tạo/đổi tên folder để tự động hiển thị node mới.
        """
        if not path_key:
            return
        parts = path_to_list(path_key)
        changed = False
        for i in range(len(parts)):
            partial = path_to_key(parts[: i + 1])
            name = parts[i]
            tree_key = f"{name}::{partial}"
            if tree_key not in self.open_folders:
                self.open_folders = [*self.open_folders, tree_key]
                changed = True
        if changed:
            self._refresh_visible()

    def collapse_all(self):
        """Đóng toàn bộ cây."""
        self.open_folders = []
        self._refresh_visible()

    def expand_all(self):
        """Mở toàn bộ cây (hữu ích khi cây nhỏ)."""
        keys = [row["tree_key"] for row in self.all_sidebar_rows if row["row_type"] == "folder"]
        self.open_folders = keys
        self._refresh_visible()