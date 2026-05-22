"""
folder_manager_state.py — State quản lý folder + bài giảng.

Chức năng:
  - Thêm / đổi tên / xoá folder con (đệ quy)
  - Thêm / đổi tên / xoá bài giảng trong folder
  - Đồng bộ sidebar (TreeState) sau mỗi thao tác
  - Breadcrumb + summary để hiển thị trên UI
"""

import reflex as rx

from HUST_Student.services.folder_service import (
    load_folders,
    flatten_folder_tree,
    path_to_list,
    path_to_key,
    rename_folder,
    delete_folder,
    add_subfolder,
)
from HUST_Student.services.studyset_service import (
    add_studyset,
    get_studysets_for_path,
    load_studysets_raw,
    remove_studyset,
    rename_studyset,
)


# ══════════════════════════════════════════════════════════════════
# STATE
# ══════════════════════════════════════════════════════════════════

class FolderManagerState(rx.State):

    # ── Selection ────────────────────────────────────────────────
    selected_path_key: str = ""
    current_folder_name: str = "Gốc"

    # ── Display data ─────────────────────────────────────────────
    tree_rows: list[dict] = []
    folder_studysets: list[dict] = []

    # ── Dialog flags ─────────────────────────────────────────────
    show_rename_dialog: bool = False
    show_add_subfolder_dialog: bool = False
    show_delete_confirmation: bool = False
    show_add_studyset_dialog: bool = False
    show_rename_studyset_dialog: bool = False
    show_delete_studyset_confirmation: bool = False

    # ── Input values ─────────────────────────────────────────────
    new_folder_name: str = ""
    new_subfolder_name: str = ""
    new_studyset_title: str = ""
    new_studyset_file: str = ""
    rename_studyset_old_title: str = ""
    rename_studyset_new_title: str = ""
    delete_studyset_title: str = ""

    # ── Feedback ─────────────────────────────────────────────────
    message: str = ""
    message_type: str = ""  # "success" | "error"

    # ════════════════════════════════════════════════════════════
    # COMPUTED VARS
    # ════════════════════════════════════════════════════════════

    @rx.var
    def is_at_root(self) -> bool:
        return self.selected_path_key == ""

    @rx.var
    def breadcrumb(self) -> str:
        if not self.selected_path_key:
            return "Gốc"
        return self.selected_path_key.replace("/", " › ")

    @rx.var
    def folder_summary(self) -> str:
        if self.is_at_root:
            return "Thư mục gốc — thêm folder con để bắt đầu"
        n_sets = len(self.folder_studysets)
        if n_sets == 0:
            return "Chưa có bài giảng nào"
        return f"{n_sets} bài giảng"

    @rx.var
    def can_rename(self) -> bool:
        return not self.is_at_root

    @rx.var
    def can_delete(self) -> bool:
        return not self.is_at_root

    @rx.var
    def can_add_studyset(self) -> bool:
        return not self.is_at_root

    # ════════════════════════════════════════════════════════════
    # INTERNAL HELPERS
    # ════════════════════════════════════════════════════════════

    async def _sync_sidebar(self):
        """Reload sidebar tree sau mọi thay đổi."""
        from HUST_Student.states.tree_state import TreeState
        from HUST_Student.states.navigation_state import NavigationState

        tree = await self.get_state(TreeState)
        tree.reload_sidebar()
        if self.selected_path_key:
            tree.expand_path(self.selected_path_key)

        nav = await self.get_state(NavigationState)
        nav.set_active_path(self.selected_path_key)

    def _rebuild_tree(self):
        data = load_folders()
        studysets = load_studysets_raw()
        self.tree_rows = flatten_folder_tree(data, studysets)

    def _load_studysets(self):
        if not self.selected_path_key:
            self.folder_studysets = []
            return
        raw = get_studysets_for_path(self.selected_path_key)
        self.folder_studysets = [
            {
                "title": s.get("title", ""),
                "file": s.get("file", ""),
                "terms": s.get("terms", 0),
                "terms_label": f"{s.get('terms', 0)} thuật ngữ",
            }
            for s in raw
        ]

    def _reload_local(self):
        self._rebuild_tree()
        if self.selected_path_key:
            path = path_to_list(self.selected_path_key)
            self.current_folder_name = path[-1] if path else "Gốc"
        else:
            self.current_folder_name = "Gốc"
        self._load_studysets()

    def _set_message(self, msg: str, msg_type: str = "success"):
        self.message = msg
        self.message_type = msg_type

    # ════════════════════════════════════════════════════════════
    # SELECTION
    # ════════════════════════════════════════════════════════════

    @rx.event
    async def load_current_folder(self, folder_path: list[str] | None = None):
        if folder_path:
            self.selected_path_key = path_to_key(folder_path)
        else:
            self.selected_path_key = ""
        self._reload_local()
        await self._sync_sidebar()

    def apply_selection(self, path_key: str):
        """Sync-call từ sidebar click, không trigger async."""
        self.selected_path_key = str(path_key) if path_key else ""
        self._reload_local()

    @rx.event
    async def select_folder(self, path_key: str):
        self.apply_selection(path_key)
        await self._sync_sidebar()

    # ════════════════════════════════════════════════════════════
    # ADD SUBFOLDER
    # ════════════════════════════════════════════════════════════

    def open_add_subfolder_dialog(self):
        self.new_subfolder_name = ""
        self.show_add_subfolder_dialog = True
        self.message = ""

    def close_add_subfolder_dialog(self):
        self.show_add_subfolder_dialog = False
        self.new_subfolder_name = ""

    def set_new_subfolder_name(self, value: str):
        self.new_subfolder_name = str(value) if value else ""

    @rx.event
    async def confirm_add_subfolder(self):
        parent_path = path_to_list(self.selected_path_key)
        name = self.new_subfolder_name.strip()

        ok, err = add_subfolder(parent_path, name)
        if ok:
            self._set_message(f"✅ Đã thêm thư mục '{name}'")
            self.close_add_subfolder_dialog()
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message(f"❌ {err}", "error")

    # ════════════════════════════════════════════════════════════
    # RENAME FOLDER
    # ════════════════════════════════════════════════════════════

    def open_rename_dialog(self):
        if self.is_at_root:
            self._set_message("❌ Chọn một thư mục để đổi tên.", "error")
            return
        self.new_folder_name = self.current_folder_name
        self.show_rename_dialog = True
        self.message = ""

    def close_rename_dialog(self):
        self.show_rename_dialog = False
        self.new_folder_name = ""

    def set_new_folder_name(self, value: str):
        self.new_folder_name = str(value) if value else ""

    @rx.event
    async def confirm_rename_folder(self):
        if self.is_at_root:
            self._set_message("❌ Không thể đổi tên thư mục gốc.", "error")
            return

        path = path_to_list(self.selected_path_key)
        new_name = self.new_folder_name.strip()

        if new_name == path[-1]:
            self.close_rename_dialog()
            return

        ok, err = rename_folder(path, new_name)
        if ok:
            self.selected_path_key = path_to_key([*path[:-1], new_name])
            self._set_message(f"✅ Đã đổi tên thành '{new_name}'")
            self.close_rename_dialog()
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message(f"❌ {err}", "error")

    # ════════════════════════════════════════════════════════════
    # DELETE FOLDER
    # ════════════════════════════════════════════════════════════

    def open_delete_confirmation(self):
        if self.is_at_root:
            self._set_message("❌ Chọn một thư mục để xoá.", "error")
            return
        self.show_delete_confirmation = True
        self.message = ""

    def close_delete_confirmation(self):
        self.show_delete_confirmation = False

    @rx.event
    async def confirm_delete_folder(self):
        if self.is_at_root:
            self._set_message("❌ Không thể xoá thư mục gốc.", "error")
            self.close_delete_confirmation()
            return

        path = path_to_list(self.selected_path_key)
        parent_key = path_to_key(path[:-1])

        ok, err = delete_folder(path)
        if ok:
            self._set_message(f"✅ Đã xoá thư mục '{path[-1]}'")
            self.close_delete_confirmation()
            self.selected_path_key = parent_key
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message(f"❌ {err}", "error")
            self.close_delete_confirmation()

    # ════════════════════════════════════════════════════════════
    # ADD STUDYSET
    # ════════════════════════════════════════════════════════════

    def open_add_studyset_dialog(self):
        if self.is_at_root:
            self._set_message("❌ Chọn một thư mục để thêm bài giảng.", "error")
            return
        self.new_studyset_title = ""
        self.new_studyset_file = ""
        self.show_add_studyset_dialog = True
        self.message = ""

    def close_add_studyset_dialog(self):
        self.show_add_studyset_dialog = False
        self.new_studyset_title = ""
        self.new_studyset_file = ""

    def set_new_studyset_title(self, value: str):
        self.new_studyset_title = str(value) if value else ""

    def set_new_studyset_file(self, value: str):
        self.new_studyset_file = str(value) if value else ""

    @rx.event
    async def confirm_add_studyset(self):
        if self.is_at_root:
            self._set_message("❌ Chọn thư mục để thêm bài giảng.", "error")
            return

        title = self.new_studyset_title.strip()
        file_path = self.new_studyset_file.strip()

        ok, err = add_studyset(self.selected_path_key, title, file_path)
        if ok:
            self._set_message(f"✅ Đã thêm bài giảng '{title}'")
            self.close_add_studyset_dialog()
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message(f"❌ {err}", "error")

    # ════════════════════════════════════════════════════════════
    # RENAME STUDYSET
    # ════════════════════════════════════════════════════════════

    def open_rename_studyset_dialog(self, title: str):
        self.rename_studyset_old_title = title
        self.rename_studyset_new_title = title
        self.show_rename_studyset_dialog = True
        self.message = ""

    def close_rename_studyset_dialog(self):
        self.show_rename_studyset_dialog = False
        self.rename_studyset_old_title = ""
        self.rename_studyset_new_title = ""

    def set_rename_studyset_new_title(self, value: str):
        self.rename_studyset_new_title = str(value) if value else ""

    @rx.event
    async def confirm_rename_studyset(self):
        old_title = self.rename_studyset_old_title
        new_title = self.rename_studyset_new_title.strip()

        ok, err = rename_studyset(self.selected_path_key, old_title, new_title)
        if ok:
            self._set_message(f"✅ Đã đổi tên thành '{new_title}'")
            self.close_rename_studyset_dialog()
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message(f"❌ {err}", "error")

    # ════════════════════════════════════════════════════════════
    # DELETE STUDYSET
    # ════════════════════════════════════════════════════════════

    def open_delete_studyset_confirmation(self, title: str):
        self.delete_studyset_title = title
        self.show_delete_studyset_confirmation = True
        self.message = ""

    def close_delete_studyset_confirmation(self):
        self.show_delete_studyset_confirmation = False
        self.delete_studyset_title = ""

    @rx.event
    async def confirm_delete_studyset(self):
        title = self.delete_studyset_title
        ok, err = remove_studyset(self.selected_path_key, title)
        if ok:
            self._set_message(f"✅ Đã xoá bài giảng '{title}'")
            self.close_delete_studyset_confirmation()
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message(f"❌ {err}", "error")
            self.close_delete_studyset_confirmation()

    @rx.event
    async def remove_studyset_item(self, title: str):
        """Quick-delete không cần confirm dialog."""
        ok, err = remove_studyset(self.selected_path_key, title)
        if ok:
            self._set_message(f"✅ Đã xoá bài giảng '{title}'")
            self._reload_local()
            await self._sync_sidebar()
        else:
            self._set_message(f"❌ {err}", "error")

    # ════════════════════════════════════════════════════════════
    # MISC
    # ════════════════════════════════════════════════════════════

    def clear_message(self):
        self.message = ""
        self.message_type = ""