import reflex as rx

from HUST_Student.states.folder_manager_state import FolderManagerState


class LibraryState(rx.State):

    current_tab: str = "hoc_phan"

    def set_hoc_phan(self):
        self.current_tab = "hoc_phan"

    def set_lop_hoc(self):
        self.current_tab = "lop_hoc"

    @rx.event
    async def set_thu_muc(self):
        from HUST_Student.states.tree_state import TreeState

        self.current_tab = "thu_muc"
        tree = await self.get_state(TreeState)
        tree.reload_sidebar()
        folder_mgr = await self.get_state(FolderManagerState)
        await folder_mgr.load_current_folder()

    def set_bai_kiem_tra(self):
        self.current_tab = "bai_kiem_tra"

    def set_loi_giai(self):
        self.current_tab = "loi_giai"