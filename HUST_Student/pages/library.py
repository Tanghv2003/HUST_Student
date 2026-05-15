import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.library_state import LibraryState
from HUST_Student.services.folder_service import load_folders
from HUST_Student.components.folder_tree import folder_node


def library_tab(
    text: str,
    active,
    on_click,
):
    return rx.box(
        rx.text(
            text,
            font_weight=rx.cond(active, "700", "500"),
            font_size="0.95rem",
            color=rx.cond(active, T.TEXT_PRIMARY, T.TEXT_SECONDARY),
        ),
        padding_bottom="0.75rem",
        border_bottom=rx.cond(
            active,
            f"3px solid {T.PRIMARY}",
            "3px solid transparent",
        ),
        cursor="pointer",
        on_click=on_click,
        _hover={"color": T.TEXT_PRIMARY},
    )


def content_card(
    title: str,
    subtitle: str,
):
    return rx.box(
        rx.vstack(
            rx.text(title, font_size="1.25rem", font_weight="700", color=T.TEXT_PRIMARY),
            rx.text(subtitle, color=T.TEXT_SECONDARY, font_size="0.9rem"),
            spacing="2",
            align="start",
        ),
        bg=T.SURFACE,
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        padding="1.35rem",
        width="100%",
        box_shadow=T.SHADOW_CARD,
        transition="box-shadow 0.15s ease, border-color 0.15s ease",
        _hover={
            "box_shadow": T.SHADOW_CARD_HOVER,
            "border_color": T.PRIMARY,
            "cursor": "pointer",
        },
    )


def hoc_phan_content():
    return rx.vstack(
        content_card(
            "Tính từ N4 thông dụng",
            "140 thuật ngữ • superTang_Ha",
        ),
        content_card(
            "Kanji N5",
            "220 thuật ngữ • No",
        ),
        spacing="4",
        width="100%",
    )


def lop_hoc_content():
    return rx.vstack(
        content_card(
            "Tiếng Nhật N5",
            "42 học viên",
        ),
        content_card(
            "Toeic 700+",
            "28 học viên",
        ),
        spacing="4",
        width="100%",
    )


def thu_muc_content():
    data = load_folders()
    return rx.vstack(
        *[
            folder_node(
                folder_name,
                children,
            )
            for folder_name, children in data.items()
        ],
        spacing="4",
        width="100%",
    )


def bai_kiem_tra_content():
    return rx.vstack(
        content_card(
            "Mini Test N5",
            "50 câu hỏi",
        ),
        content_card(
            "Toeic Listening Test",
            "100 câu hỏi",
        ),
        spacing="4",
        width="100%",
    )


def loi_giai_content():
    return rx.vstack(
        content_card(
            "Giải bài tập Kanji",
            "Giải thích chi tiết từng câu",
        ),
        content_card(
            "Toeic Reading Solutions",
            "Chiến thuật làm bài",
        ),
        spacing="4",
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
        rx.text(
            "Thư viện của bạn",
            font_size="2.25rem",
            font_weight="800",
            color=T.TEXT_PRIMARY,
            letter_spacing="-0.02em",
        ),
        rx.hstack(
            library_tab(
                "Học phần",
                LibraryState.current_tab == "hoc_phan",
                LibraryState.set_hoc_phan,
            ),
            library_tab(
                "Lớp học",
                LibraryState.current_tab == "lop_hoc",
                LibraryState.set_lop_hoc,
            ),
            library_tab(
                "Thư mục",
                LibraryState.current_tab == "thu_muc",
                LibraryState.set_thu_muc,
            ),
            library_tab(
                "Bài kiểm tra thử",
                LibraryState.current_tab == "bai_kiem_tra",
                LibraryState.set_bai_kiem_tra,
            ),
            library_tab(
                "Lời giải chuyên gia",
                LibraryState.current_tab == "loi_giai",
                LibraryState.set_loi_giai,
            ),
            spacing="7",
            width="100%",
            border_bottom=f"1px solid {T.BORDER_LIGHT}",
        ),
        rx.hstack(
            rx.spacer(),
            rx.input(
                placeholder="Tìm kiếm...",
                width="420px",
                bg=T.SURFACE,
                border=f"1px solid {T.BORDER}",
                color=T.TEXT_PRIMARY,
                border_radius=T.RADIUS_MD,
                height="44px",
                padding_x="1rem",
                size="3",
                _focus={
                    "border_color": T.PRIMARY,
                    "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                },
            ),
            width="100%",
        ),
        library_content_router(),
        spacing="7",
        width="100%",
    )
