import reflex as rx


class TreeState(rx.State):
    """Quản lý trạng thái mở/đóng accordion trong cây thư mục."""

    open_folders: list[str] = []

    def toggle_folder(self, key: str):
        if key in self.open_folders:
            self.open_folders = [k for k in self.open_folders if k != key]
        else:
            self.open_folders = self.open_folders + [key]

    def expand_folder(self, key: str):
        if key not in self.open_folders:
            self.open_folders = self.open_folders + [key]

    def collapse_all(self):
        self.open_folders = []