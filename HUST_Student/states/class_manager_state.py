import reflex as rx

from HUST_Student.services.class_service import (
    load_classes,
    flatten_class_tree,
    path_to_list,
    path_to_key,
    rename_class,
    delete_class,
    add_subclass,
)
from HUST_Student.services.class_lesson_service import (
    add_lesson,
    get_lessons_for_path,
    load_class_lessons_raw,
    remove_lesson,
)


class ClassManagerState(rx.State):
    """Quản lý lớp học — lớp chứa lớp con; bài giảng JSON trong class_lessons.json."""

    selected_path_key: str = ""
    current_class_name: str = "Gốc"

    tree_rows: list[dict] = []
    class_lessons: list[dict] = []

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

    @rx.var
    def is_at_root(self) -> bool:
        return self.selected_path_key == ""

    @rx.var
    def breadcrumb(self) -> str:
        if not self.selected_path_key:
            return "Gốc"
        return self.selected_path_key.replace("/", " / ")

    @rx.var
    def class_summary(self) -> str:
        if self.is_at_root:
            return "Thêm lớp học gốc hoặc chọn lớp trong cây"
        return f"{len(self.class_lessons)} bài giảng trong lớp này"

    async def _sync_class_tree(self):
        from HUST_Student.states.kanji_state import ClassTreeState

        tree = await self.get_state(ClassTreeState)
        tree.reload_class_tree()
        if self.selected_path_key:
            tree.expand_path(self.selected_path_key)
        tree.set_active_path(self.selected_path_key)

    def _rebuild_tree(self):
        data = load_classes()
        lessons = load_class_lessons_raw()
        self.tree_rows = flatten_class_tree(data, lessons)

    def _load_lessons(self):
        if not self.selected_path_key:
            self.class_lessons = []
            return
        self.class_lessons = [
            {
                "title": item.get("title", ""),
                "file": item.get("file", ""),
                "terms": item.get("terms", 0),
                "terms_label": f"{item.get('terms', 0)} mục",
            }
            for item in get_lessons_for_path(self.selected_path_key)
        ]

    def _load_selected_class(self):
        self._rebuild_tree()
        if not self.selected_path_key:
            self.current_class_name = "Gốc"
            self._load_lessons()
            return
        path = path_to_list(self.selected_path_key)
        self.current_class_name = path[-1]
        self._load_lessons()

    @rx.event
    async def load_current_class(self, class_path: list[str] | None = None):
        if class_path is None or not class_path:
            self.selected_path_key = ""
        else:
            self.selected_path_key = path_to_key(class_path)
        self._load_selected_class()
        await self._sync_class_tree()

    def apply_selection(self, path_key: str):
        self.selected_path_key = str(path_key) if path_key else ""
        self._load_selected_class()

    @rx.event
    async def select_class(self, path_key: str):
        self.apply_selection(path_key)
        await self._sync_class_tree()

    def open_rename_dialog(self):
        if self.is_at_root:
            return
        self.new_class_name = self.current_class_name
        self.show_rename_dialog = True

    def close_rename_dialog(self):
        self.show_rename_dialog = False
        self.new_class_name = ""

    def set_new_class_name(self, value: str):
        self.new_class_name = str(value) if value else ""

    @rx.event
    async def confirm_rename_class(self):
        if self.is_at_root:
            self.message = "❌ Chọn một lớp để đổi tên"
            self.message_type = "error"
            return
        if not self.new_class_name.strip():
            self.message = "❌ Tên lớp không được để trống"
            self.message_type = "error"
            return

        path = path_to_list(self.selected_path_key)
        new_name = self.new_class_name.strip()
        if new_name == path[-1]:
            self.close_rename_dialog()
            return

        if rename_class(path, new_name):
            self.selected_path_key = path_to_key([*path[:-1], new_name])
            self.message = f"✅ Đổi tên lớp: {new_name}"
            self.message_type = "success"
            self.close_rename_dialog()
            self._load_selected_class()
            await self._sync_class_tree()
        else:
            self.message = "❌ Lỗi đổi tên (có thể trùng tên)"
            self.message_type = "error"

    def open_delete_confirmation(self):
        if self.is_at_root:
            return
        self.show_delete_confirmation = True

    def close_delete_confirmation(self):
        self.show_delete_confirmation = False

    @rx.event
    async def confirm_delete_class(self):
        if self.is_at_root:
            self.message = "❌ Chọn một lớp để xóa"
            self.message_type = "error"
            self.close_delete_confirmation()
            return

        path = path_to_list(self.selected_path_key)
        parent_key = path_to_key(path[:-1])

        if delete_class(path):
            self.message = "✅ Xóa lớp thành công"
            self.message_type = "success"
            self.close_delete_confirmation()
            self.selected_path_key = parent_key
            self._load_selected_class()
            await self._sync_class_tree()
        else:
            self.message = "❌ Lỗi khi xóa lớp"
            self.message_type = "error"
            self.close_delete_confirmation()

    def open_add_subclass_dialog(self):
        self.new_subclass_name = ""
        self.show_add_subclass_dialog = True

    def close_add_subclass_dialog(self):
        self.show_add_subclass_dialog = False
        self.new_subclass_name = ""

    def set_new_subclass_name(self, value: str):
        self.new_subclass_name = str(value) if value else ""

    @rx.event
    async def confirm_add_subclass(self):
        if not self.new_subclass_name.strip():
            self.message = "❌ Tên lớp con không được để trống"
            self.message_type = "error"
            return

        parent_path = path_to_list(self.selected_path_key)
        name = self.new_subclass_name.strip()

        if add_subclass(parent_path, name):
            self.message = f"✅ Thêm lớp con '{name}' thành công"
            self.message_type = "success"
            self.close_add_subclass_dialog()
            self._load_selected_class()
            await self._sync_class_tree()
        else:
            self.message = "❌ Lỗi thêm lớp con (có thể trùng tên)"
            self.message_type = "error"

    def open_add_lesson_dialog(self):
        if self.is_at_root:
            return
        self.new_lesson_title = ""
        self.new_lesson_file = ""
        self.show_add_lesson_dialog = True

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
            self.message = "❌ Chọn lớp để thêm bài giảng"
            self.message_type = "error"
            return
        if not self.new_lesson_title.strip() or not self.new_lesson_file.strip():
            self.message = "❌ Tên và file JSON không được trống"
            self.message_type = "error"
            return

        if add_lesson(
            self.selected_path_key,
            self.new_lesson_title.strip(),
            self.new_lesson_file.strip(),
        ):
            self.message = "✅ Thêm bài giảng thành công"
            self.message_type = "success"
            self.close_add_lesson_dialog()
            self._load_selected_class()
            await self._sync_class_tree()
        else:
            self.message = "❌ Không thể thêm (có thể trùng tên)"
            self.message_type = "error"

    @rx.event
    async def remove_lesson_item(self, title: str):
        if not self.selected_path_key:
            return
        if remove_lesson(self.selected_path_key, title):
            self.message = "✅ Đã xóa bài giảng"
            self.message_type = "success"
            self._load_selected_class()
            await self._sync_class_tree()
        else:
            self.message = "❌ Lỗi khi xóa bài giảng"
            self.message_type = "error"

    def clear_message(self):
        self.message = ""
        self.message_type = ""
