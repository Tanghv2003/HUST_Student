import reflex as rx

from HUST_Student.states.library_state import LibraryState
from HUST_Student.services.folder_service import load_folders
from HUST_Student.components.folder_tree import folder_node


# =========================================
# TAB BUTTON
# =========================================

def library_tab(
    text: str,
    active,
    on_click,
):

    return rx.box(

        rx.text(
            text,

            font_weight=rx.cond(
                active,
                "700",
                "500",
            ),

            color=rx.cond(
                active,
                "#111827",
                "#6B7280",
            ),
        ),

        padding_bottom="0.8rem",

        border_bottom=rx.cond(
            active,
            "3px solid #4F46E5",
            "3px solid transparent",
        ),

        cursor="pointer",

        on_click=on_click,
    )


# =========================================
# CONTENT CARD
# =========================================

def content_card(
    title: str,
    subtitle: str,
):

    return rx.box(

        rx.vstack(

            rx.text(
                title,
                font_size="1.5rem",
                font_weight="700",
            ),

            rx.text(
                subtitle,
                color="#6B7280",
            ),

            spacing="2",

            align="start",
        ),

        bg="white",

        border="1px solid #E5E7EB",

        border_radius="18px",

        padding="1.5rem",

        width="100%",

        _hover={
            "box_shadow": "0 4px 12px rgba(0,0,0,0.06)",
        },
    )


# =========================================
# TAB CONTENTS
# =========================================

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


# =========================================
# ROUTER
# =========================================

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


# =========================================
# PAGE
# =========================================

def library_page():

    return rx.vstack(

        rx.text(
            "Thư viện của bạn",
            font_size="3rem",
            font_weight="700",
        ),

        # TABS
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
        ),

        rx.divider(),

        # SEARCH
        rx.hstack(

            rx.spacer(),

            rx.input(
                placeholder="Tìm kiếm...",

                width="420px",

                bg="white",

                border="1px solid #E5E7EB",

                border_radius="14px",

                size="3",
            ),

            width="100%",
        ),

        # CONTENT
        library_content_router(),

        spacing="7",

        width="100%",
    )