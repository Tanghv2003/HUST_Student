import reflex as rx


class NavigationState(rx.State):

    current_page: str = "home"

    current_folder: str = ""

    # =========================
    # HOME
    # =========================

    def go_home(self):

        self.current_page = "home"

    # =========================
    # LIBRARY
    # =========================

    def go_library(self):

        self.current_page = "library"

    # =========================
    # CLASSES
    # =========================

    def go_classes(self):

        self.current_page = "classes"

    # =========================
    # FOLDER DETAIL
    # =========================

    def set_folder_detail(
        self,
        folder_name: str,
    ):

        self.current_page = "folder_detail"

        self.current_folder = folder_name

    # =========================
    # GENERIC
    # =========================

    def set_page(
        self,
        page: str,
    ):

        self.current_page = page