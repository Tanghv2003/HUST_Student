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
)


class FolderManagerState(rx.State):
    """Quản lý folder — folder chỉ chứa thư mục con; bài giảng có JSON trong studysets.json."""

    selected_path_key: str = ""
    current_folder_name: str = "Gốc"

    tree_rows: list[dict] = []
    folder_studysets: list[dict] = []

    show_rename_dialog: bool = False
    show_add_subfolder_dialog: bool = False
    show_delete_confirmation: bool = False
    show_add_studyset_dialog: bool = False

    new_folder_name: str = ""
    new_subfolder_name: str = ""
    new_studyset_title: str = ""
    new_studyset_file: str = ""

    message: str = ""
    message_type: str = ""

    @rx.var
    def is_at_root(self) -> bool:
        return self.selected_path_key == ""

    @rx.var
    def breadcrumb(self) -> str:
        if not self.selected_path_key:
            return "Gốc"
        return self.selected_path_key.replace("/", " / ")

    @rx.var
    def folder_summary(self) -> str:
        if self.is_at_root:
            return "Thư mục gốc — thêm folder hoặc chọn folder con"
        n = len(self.folder_studysets)
        return f"{n} bài giảng trong thư mục này"

    async def _sync_sidebar(self):
        from HUST_Student.states.navigation_state import NavigationState
        from HUST_Student.states.tree_state import TreeState

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
        self.folder_studysets = [
            {
                "title": s.get("title", ""),
                "file": s.get("file", ""),
                "terms": s.get("terms", 0),
                "terms_label": f"{s.get('terms', 0)} thuật ngữ",
            }
            for s in get_studysets_for_path(self.selected_path_key)
        ]

    def _load_selected_folder(self):
        self._rebuild_tree()

        if not self.selected_path_key:
            self.current_folder_name = "Gốc"
            self._load_studysets()
            return

        path = path_to_list(self.selected_path_key)
        self.current_folder_name = path[-1]
        self._load_studysets()

    @rx.event
    async def load_current_folder(self, folder_path: list[str] | None = None):
        if folder_path is None or not folder_path:
            self.selected_path_key = ""
        else:
            self.selected_path_key = path_to_key(folder_path)
        self._load_selected_folder()
        await self._sync_sidebar()

    def apply_selection(self, path_key: str):
        """Cập nhật chọn folder (sync) — dùng từ sidebar."""
        self.selected_path_key = str(path_key) if path_key else ""
        self._load_selected_folder()

    @rx.event
    async def select_folder(self, path_key: str):
        self.apply_selection(path_key)
        await self._sync_sidebar()

    def open_rename_dialog(self):
        if self.is_at_root:
            return
        self.new_folder_name = self.current_folder_name
        self.show_rename_dialog = True

    def close_rename_dialog(self):
        self.show_rename_dialog = False
        self.new_folder_name = ""

    def set_new_folder_name(self, value: str):
        self.new_folder_name = str(value) if value else ""

    @rx.event
    async def confirm_rename_folder(self):
        if self.is_at_root:
            self.message = "❌ Chọn một thư mục để đổi tên"
            self.message_type = "error"
            return

        if not self.new_folder_name.strip():
            self.message = "❌ Tên folder không được để trống"
            self.message_type = "error"
            return

        path = path_to_list(self.selected_path_key)
        new_name = self.new_folder_name.strip()
        if new_name == path[-1]:
            self.close_rename_dialog()
            return

        if rename_folder(path, new_name):
            self.selected_path_key = path_to_key([*path[:-1], new_name])
            self.message = f"✅ Đổi tên thành công: {new_name}"
            self.message_type = "success"
            self.close_rename_dialog()
            self._load_selected_folder()
            await self._sync_sidebar()
        else:
            self.message = "❌ Lỗi khi đổi tên (tên có thể đã tồn tại)"
            self.message_type = "error"

    def open_delete_confirmation(self):
        if self.is_at_root:
            return
        self.show_delete_confirmation = True

    def close_delete_confirmation(self):
        self.show_delete_confirmation = False

    @rx.event
    async def confirm_delete_folder(self):
        if self.is_at_root:
            self.message = "❌ Chọn một thư mục để xóa"
            self.message_type = "error"
            self.close_delete_confirmation()
            return

        path = path_to_list(self.selected_path_key)
        parent_key = path_to_key(path[:-1])

        if delete_folder(path):
            self.message = "✅ Xóa folder thành công"
            self.message_type = "success"
            self.close_delete_confirmation()
            self.selected_path_key = parent_key
            self._load_selected_folder()
            await self._sync_sidebar()
        else:
            self.message = "❌ Lỗi khi xóa folder"
            self.message_type = "error"
            self.close_delete_confirmation()

    def open_add_subfolder_dialog(self):
        self.new_subfolder_name = ""
        self.show_add_subfolder_dialog = True

    def close_add_subfolder_dialog(self):
        self.show_add_subfolder_dialog = False
        self.new_subfolder_name = ""

    def set_new_subfolder_name(self, value: str):
        self.new_subfolder_name = str(value) if value else ""

    @rx.event
    async def confirm_add_subfolder(self):
        if not self.new_subfolder_name.strip():
            self.message = "❌ Tên folder con không được để trống"
            self.message_type = "error"
            return

        parent_path = path_to_list(self.selected_path_key)
        name = self.new_subfolder_name.strip()

        if add_subfolder(parent_path, name):
            self.message = f"✅ Thêm folder con '{name}' thành công"
            self.message_type = "success"
            self.close_add_subfolder_dialog()
            self._load_selected_folder()
            await self._sync_sidebar()
        else:
            self.message = "❌ Lỗi khi thêm folder con (có thể tên đã tồn tại)"
            self.message_type = "error"

    def open_add_studyset_dialog(self):
        if self.is_at_root:
            return
        self.new_studyset_title = ""
        self.new_studyset_file = ""
        self.show_add_studyset_dialog = True

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
            self.message = "❌ Chọn thư mục để thêm bài giảng"
            self.message_type = "error"
            return
        if not self.new_studyset_title.strip() or not self.new_studyset_file.strip():
            self.message = "❌ Tên và file JSON bài giảng không được trống"
            self.message_type = "error"
            return

        if add_studyset(
            self.selected_path_key,
            self.new_studyset_title.strip(),
            self.new_studyset_file.strip(),
        ):
            self.message = f"✅ Thêm bài giảng thành công"
            self.message_type = "success"
            self.close_add_studyset_dialog()
            self._load_selected_folder()
            await self._sync_sidebar()
        else:
            self.message = "❌ Không thể thêm (có thể trùng tên)"
            self.message_type = "error"

    @rx.event
    async def remove_studyset_item(self, title: str):
        if not self.selected_path_key:
            return
        if remove_studyset(self.selected_path_key, title):
            self.message = f"✅ Đã xóa bài giảng"
            self.message_type = "success"
            self._load_selected_folder()
            await self._sync_sidebar()
        else:
            self.message = "❌ Lỗi khi xóa bài giảng"
            self.message_type = "error"

    def clear_message(self):
        self.message = ""
        self.message_type = ""
