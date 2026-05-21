import reflex as rx


class NavigationState(rx.State):

    current_page: str = "home"
    current_folder: str = ""
    current_path_key: str = ""

    def go_home(self):
        self.current_page = "home"

    @rx.event
    async def go_library(self):
        from HUST_Student.states.tree_state import TreeState

        self.current_page = "library"
        tree = await self.get_state(TreeState)
        tree.reload_sidebar()

    def go_classes(self):
        self.current_page = "classes"

    def go_conversation(self):
        self.current_page = "conversation"

    def set_folder_detail(self, folder_name: str):
        self.current_page = "folder_detail"
        self.current_folder = folder_name

    def set_active_path(self, path_key: str):
        """Cập nhật folder đang chọn (không đổi trang)."""
        self.current_path_key = path_key or ""
        parts = path_key.split("/") if path_key else []
        self.current_folder = parts[-1] if parts else ""

    def set_folder_detail_path(self, path_key: str):
        self.current_page = "folder_detail"
        self.set_active_path(path_key)

    def set_page(self, page: str):
        self.current_page = page
