import reflex as rx

from HUST_Student.components.sidebar import sidebar
from HUST_Student.components.topbar import topbar
from HUST_Student.components.ui import theme as T

from HUST_Student.pages.library import library_page
from HUST_Student.pages.classes import classes_page
from HUST_Student.pages.folder_detail import folder_detail_page
from HUST_Student.pages.conversation import conversation_page

from HUST_Student.states.navigation_state import NavigationState


def homepage_content():
    return rx.vstack(
        rx.text("Trang chủ", font_size="2rem", font_weight="700", color=T.TEXT_PRIMARY),
        rx.text(
            "Chọn Thư viện, Luyện hội thoại hoặc Lớp học từ thanh bên để bắt đầu.",
            color=T.TEXT_SECONDARY,
            font_size="1rem",
            margin_top="0.5rem",
        ),
        width="100%",
        align="start",
        spacing="2",
        padding_top="0.5rem",
    )


def content_router():
    return rx.cond(
        NavigationState.current_page == "home",
        homepage_content(),
        rx.cond(
            NavigationState.current_page == "library",
            library_page(),
            rx.cond(
                NavigationState.current_page == "folder_detail",
                folder_detail_page(),
                rx.cond(
                    NavigationState.current_page == "conversation",
                    conversation_page(),
                    classes_page(),
                ),
            ),
        ),
    )


def home():
    return rx.box(
        sidebar(),
        rx.box(
            rx.vstack(
                topbar(),
                content_router(),
                spacing="8",
                width="100%",
            ),
            margin_left="280px",
            padding="1.75rem 2.25rem",
            bg=T.PAGE_BG,
            min_height="100vh",
        ),
    )
