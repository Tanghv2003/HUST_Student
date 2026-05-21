import reflex as rx

from HUST_Student.services.folder_service import (
    build_sidebar_rows,
    load_folders,
    path_to_key,
    path_to_list,
)
from HUST_Student.services.studyset_service import load_studysets


class TreeState(rx.State):
    """Cây thư mục sidebar — reactive, đồng bộ với folders.json & studysets.json."""

    open_folders: list[str] = []
    all_sidebar_rows: list[dict] = []
    visible_sidebar_rows: list[dict] = []

    def _refresh_visible(self):
        open_set = set(self.open_folders)
        self.visible_sidebar_rows = [
            row
            for row in self.all_sidebar_rows
            if row["level"] == 0 or row["parent_tree_key"] in open_set
        ]

    def reload_sidebar(self):
        folders = load_folders()
        studysets = load_studysets()
        self.all_sidebar_rows = build_sidebar_rows(folders, studysets)
        self._refresh_visible()

    def toggle_folder(self, key: str):
        if key in self.open_folders:
            self.open_folders = [k for k in self.open_folders if k != key]
        else:
            self.open_folders = [*self.open_folders, key]
        self._refresh_visible()

    def expand_folder(self, key: str):
        if key not in self.open_folders:
            self.open_folders = [*self.open_folders, key]
            self._refresh_visible()

    def expand_path(self, path_key: str):
        """Mở rộng mọi folder cha của path_key."""
        if not path_key:
            return
        parts = path_to_list(path_key)
        for i in range(len(parts)):
            partial = path_to_key(parts[: i + 1])
            name = parts[i]
            self.expand_folder(f"{name}::{partial}")

    def collapse_all(self):
        self.open_folders = []
        self._refresh_visible()
