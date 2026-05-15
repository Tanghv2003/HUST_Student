import reflex as rx

from HUST_Student.components.ui import theme as T


def class_card(
    title: str,
    students: str,
    color: str,
):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    width="14px",
                    height="14px",
                    border_radius="999px",
                    bg=color,
                ),
                rx.text(
                    title,
                    font_weight="700",
                    font_size="1.15rem",
                    color=T.TEXT_PRIMARY,
                ),
                spacing="3",
                align="center",
            ),
            rx.text(students, color=T.TEXT_SECONDARY, font_size="0.9rem"),
            rx.button(
                "Vào lớp",
                bg=T.PRIMARY,
                color="white",
                font_weight="700",
                border_radius=T.RADIUS_MD,
                padding_x="1.25rem",
                _hover={"bg": T.PRIMARY_HOVER},
            ),
            spacing="4",
            align="start",
        ),
        bg=T.SURFACE,
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        padding="1.5rem",
        width="320px",
        box_shadow=T.SHADOW_CARD,
        transition="box-shadow 0.15s ease",
        _hover={"box_shadow": T.SHADOW_CARD_HOVER},
    )


def classes_page():
    return rx.vstack(
        rx.hstack(
            rx.text(
                "Lớp học của tôi",
                font_size="2.25rem",
                font_weight="800",
                color=T.TEXT_PRIMARY,
                letter_spacing="-0.02em",
            ),
            rx.spacer(),
            rx.button(
                "+ Tạo lớp học",
                bg=T.PRIMARY,
                color="white",
                font_weight="700",
                border_radius=T.RADIUS_MD,
                padding_x="1.25rem",
                _hover={"bg": T.PRIMARY_HOVER},
            ),
            width="100%",
        ),
        rx.grid(
            class_card(
                "Tiếng Nhật N5",
                "42 học viên",
                "#23B26D",
            ),
            class_card(
                "Toeic 700+",
                "28 học viên",
                T.PRIMARY,
            ),
            class_card(
                "Kanji N4",
                "35 học viên",
                "#E879F9",
            ),
            class_card(
                "Ngữ pháp N3",
                "19 học viên",
                T.WARN,
            ),
            columns="2",
            spacing="6",
            width="100%",
        ),
        spacing="7",
        width="100%",
    )
