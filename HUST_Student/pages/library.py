import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.library_state import LibraryState
from HUST_Student.services.folder_service import load_folders
from HUST_Student.components.folder_tree import folder_node


def library_tab(text: str, active, on_click):
    return rx.box(
        rx.text(
            text,
            font_weight=rx.cond(active, "700", "500"),
            font_size="0.875rem",
            color=rx.cond(active, T.PRIMARY, T.TEXT_SECONDARY),
            white_space="nowrap",
        ),
        padding_bottom="0.6rem",
        border_bottom=rx.cond(active, f"2.5px solid {T.PRIMARY}", "2.5px solid transparent"),
        cursor="pointer",
        on_click=on_click,
        _hover={"color": T.TEXT_PRIMARY},
        flex_shrink="0",
    )


def content_card(title: str, subtitle: str, icon: str = "book"):
    return rx.hstack(
        rx.box(
            rx.icon(icon, size=18, color=T.PRIMARY),
            bg=T.PRIMARY_TINT,
            border_radius=T.RADIUS_MD,
            padding="0.6rem",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(title, font_size="0.95rem", font_weight="700", color=T.TEXT_PRIMARY, no_of_lines=1),
            rx.text(subtitle, color=T.TEXT_MUTED, font_size="0.8rem"),
            spacing="0",
            align="start",
        ),
        rx.spacer(),
        rx.icon("chevron-right", size=16, color=T.TEXT_MUTED),
        align="center",
        spacing="3",
        width="100%",
        padding="0.85rem 1rem",
        bg=T.SURFACE,
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        cursor="pointer",
        transition="all 0.12s ease",
        _hover={
            "box_shadow": T.SHADOW_CARD_HOVER,
            "border_color": T.PRIMARY,
        },
    )


def hoc_phan_content():
    return rx.vstack(
        content_card("Tính từ N4 thông dụng", "140 thuật ngữ • superTang_Ha", "book"),
        content_card("Kanji N5", "220 thuật ngữ • No", "book"),
        spacing="2",
        width="100%",
    )


def lop_hoc_content():
    return rx.vstack(
        content_card("Tiếng Nhật N5", "42 học viên", "users"),
        content_card("Toeic 700+", "28 học viên", "users"),
        spacing="2",
        width="100%",
    )


def thu_muc_content():
    """Cây thư mục — hiển thị accordion với studysets inline."""
    try:
        data = load_folders()
    except Exception:
        data = {}

    return rx.box(
        rx.vstack(
            *[
                folder_node(folder_name, children)
                for folder_name, children in data.items()
            ],
            spacing="1",
            width="100%",
        ),
        width="100%",
        overflow_y="auto",
    )


def bai_kiem_tra_content():
    return rx.vstack(
        content_card("Mini Test N5", "50 câu hỏi", "clipboard-check"),
        content_card("Toeic Listening Test", "100 câu hỏi", "clipboard-check"),
        spacing="2",
        width="100%",
    )


def loi_giai_content():
    return rx.vstack(
        content_card("Giải bài tập Kanji", "Giải thích chi tiết từng câu", "lightbulb"),
        content_card("Toeic Reading Solutions", "Chiến thuật làm bài", "lightbulb"),
        spacing="2",
        width="100%",
    )


def library_content_router():
    return rx.cond(
        LibraryState.current_tab == "hoc_phan",
        hoc_phan_content(),
        rx.cond(
            LibraryState.current_tab == "lop_hoc",
            lop_hoc_content(),
            rx.cond(
                LibraryState.current_tab == "thu_muc",
                thu_muc_content(),
                rx.cond(
                    LibraryState.current_tab == "bai_kiem_tra",
                    bai_kiem_tra_content(),
                    loi_giai_content(),
                ),
            ),
        ),
    )


def library_page():
    return rx.vstack(
        # Header
        rx.hstack(
            rx.text(
                "Thư viện",
                font_size="1.5rem",
                font_weight="800",
                color=T.TEXT_PRIMARY,
                letter_spacing="-0.02em",
            ),
            rx.spacer(),
            rx.input(
                placeholder="Tìm kiếm...",
                width="200px",
                bg=T.SURFACE,
                border=f"1px solid {T.BORDER}",
                color=T.TEXT_PRIMARY,
                border_radius=T.RADIUS_MD,
                height="36px",
                padding_x="0.9rem",
                size="2",
                _focus={
                    "border_color": T.PRIMARY,
                    "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                },
            ),
            width="100%",
            align="center",
        ),

        # Tabs (scrollable row, no wrap)
        rx.hstack(
            library_tab("Học phần", LibraryState.current_tab == "hoc_phan", LibraryState.set_hoc_phan),
            library_tab("Lớp học", LibraryState.current_tab == "lop_hoc", LibraryState.set_lop_hoc),
            library_tab("Thư mục", LibraryState.current_tab == "thu_muc", LibraryState.set_thu_muc),
            library_tab("Bài kiểm tra", LibraryState.current_tab == "bai_kiem_tra", LibraryState.set_bai_kiem_tra),
            library_tab("Lời giải", LibraryState.current_tab == "loi_giai", LibraryState.set_loi_giai),
            spacing="5",
            width="100%",
            border_bottom=f"1px solid {T.BORDER_LIGHT}",
            overflow_x="auto",
        ),

        # Content area — chiếm không gian còn lại
        rx.box(
            library_content_router(),
            flex="1",
            width="100%",
            overflow_y="auto",
        ),

        spacing="3",
        width="100%",
        height="100%",
        align="start",
    )