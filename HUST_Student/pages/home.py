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
        rx.vstack(
            rx.text(
                "Chào mừng trở lại! 👋",
                font_size="1.75rem",
                font_weight="800",
                color=T.TEXT_PRIMARY,
                letter_spacing="-0.02em",
            ),
            rx.text(
                "Chọn Thư viện, Luyện hội thoại hoặc Lớp học từ thanh bên để bắt đầu.",
                color=T.TEXT_SECONDARY,
                font_size="0.95rem",
            ),
            spacing="2",
            align="start",
        ),
        # Quick stats cards
        rx.hstack(
            rx.box(
                rx.vstack(
                    rx.icon("book", size=24, color=T.PRIMARY),
                    rx.text("Học phần", font_size="0.8rem", color=T.TEXT_SECONDARY, font_weight="500"),
                    rx.text("4", font_size="1.5rem", font_weight="800", color=T.TEXT_PRIMARY),
                    spacing="2",
                    align="center",
                ),
                bg=T.SURFACE,
                border=f"1px solid {T.BORDER}",
                border_radius=T.RADIUS_LG,
                padding="1.25rem",
                flex="1",
                text_align="center",
                box_shadow=T.SHADOW_CARD,
            ),
            rx.box(
                rx.vstack(
                    rx.icon("graduation-cap", size=24, color=T.SUCCESS),
                    rx.text("Lớp học", font_size="0.8rem", color=T.TEXT_SECONDARY, font_weight="500"),
                    rx.text("4", font_size="1.5rem", font_weight="800", color=T.TEXT_PRIMARY),
                    spacing="2",
                    align="center",
                ),
                bg=T.SURFACE,
                border=f"1px solid {T.BORDER}",
                border_radius=T.RADIUS_LG,
                padding="1.25rem",
                flex="1",
                text_align="center",
                box_shadow=T.SHADOW_CARD,
            ),
            rx.box(
                rx.vstack(
                    rx.icon("zap", size=24, color=T.WARN),
                    rx.text("Chuỗi học", font_size="0.8rem", color=T.TEXT_SECONDARY, font_weight="500"),
                    rx.text("7 ngày", font_size="1.5rem", font_weight="800", color=T.TEXT_PRIMARY),
                    spacing="2",
                    align="center",
                ),
                bg=T.SURFACE,
                border=f"1px solid {T.BORDER}",
                border_radius=T.RADIUS_LG,
                padding="1.25rem",
                flex="1",
                text_align="center",
                box_shadow=T.SHADOW_CARD,
            ),
            spacing="4",
            width="100%",
        ),
        spacing="6",
        width="100%",
        align="start",
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
        # Main content area — fixed height, no page scroll
        rx.box(
            rx.vstack(
                topbar(),
                rx.box(
                    content_router(),
                    flex="1",
                    width="100%",
                    overflow_y="auto",
                    padding_top="0.25rem",
                ),
                spacing="0",
                width="100%",
                height="100%",
                gap="0",
            ),
            margin_left="260px",
            padding="1.5rem 2rem 1rem",
            bg=T.PAGE_BG,
            height="100vh",
            overflow="hidden",
            display="flex",
            flex_direction="column",
        ),
        position="relative",
        width="100%",
        min_height="100vh",
    )