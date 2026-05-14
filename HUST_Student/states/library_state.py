import reflex as rx


class LibraryState(rx.State):

    current_tab: str = "hoc_phan"

    def set_hoc_phan(self):
        self.current_tab = "hoc_phan"

    def set_lop_hoc(self):
        self.current_tab = "lop_hoc"

    def set_thu_muc(self):
        self.current_tab = "thu_muc"

    def set_bai_kiem_tra(self):
        self.current_tab = "bai_kiem_tra"

    def set_loi_giai(self):
        self.current_tab = "loi_giai"