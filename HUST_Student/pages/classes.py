import reflex as rx

from HUST_Student.components.ui import theme as T


def class_card(title: str, students: str, color: str, icon: str = "users"):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(icon, size=16, color=color),
                    bg=color + "18",
                    border_radius=T.RADIUS_MD,
                    padding="0.5rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.spacer(),
                rx.box(
                    width="8px",
                    height="8px",
                    border_radius="999px",
                    bg=T.SUCCESS,
                    box_shadow=f"0 0 0 3px {T.SUCCESS}22",
                ),
                width="100%",
                align="center",
            ),
            rx.vstack(
                rx.text(title, font_weight="700", font_size="1rem", color=T.TEXT_PRIMARY, no_of_lines=1),
                rx.text(students, color=T.TEXT_SECONDARY, font_size="0.82rem"),
                spacing="1",
                align="start",
            ),
            rx.hstack(
                rx.button(
                    "Vào lớp",
                    bg=color,
                    color="white",
                    font_weight="600",
                    font_size="0.8rem",
                    border_radius=T.RADIUS_MD,
                    padding_x="1rem",
                    height="32px",
                    _hover={"opacity": "0.88", "cursor": "pointer"},
                ),
                rx.spacer(),
                rx.icon("arrow-right", size=16, color=T.TEXT_MUTED),
                width="100%",
                align="center",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        bg=T.SURFACE,
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        padding="1.1rem 1.2rem",
        box_shadow=T.SHADOW_CARD,
        transition="all 0.12s ease",
        _hover={
            "box_shadow": T.SHADOW_CARD_HOVER,
            "border_color": color,
            "transform": "translateY(-1px)",
        },
        cursor="pointer",
    )


def classes_page():
    return rx.vstack(
        # Header
        rx.hstack(
            rx.vstack(
                rx.text(
                    "Lớp học của tôi",
                    font_size="1.5rem",
                    font_weight="800",
                    color=T.TEXT_PRIMARY,
                    letter_spacing="-0.02em",
                ),
                rx.text("4 lớp đang tham gia", font_size="0.85rem", color=T.TEXT_SECONDARY),
                spacing="0",
                align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=15),
                    rx.text("Tạo lớp", font_size="0.875rem", font_weight="600"),
                    spacing="2",
                    align="center",
                ),
                bg=T.PRIMARY,
                color="white",
                border_radius=T.RADIUS_MD,
                padding_x="1rem",
                height="36px",
                _hover={"bg": T.PRIMARY_HOVER},
            ),
            width="100%",
            align="center",
        ),

        # Grid 2x2
        rx.grid(
            class_card("Tiếng Nhật N5", "42 học viên", "#23B26D", "users"),
            class_card("Toeic 700+", "28 học viên", T.PRIMARY, "users"),
            class_card("Kanji N4", "35 học viên", "#E879F9", "users"),
            class_card("Ngữ pháp N3", "19 học viên", T.WARN, "users"),
            template_columns="repeat(2, minmax(0, 1fr))",
            gap="4",
            width="100%",
        ),

        spacing="4",
        width="100%",
        height="100%",
        align="start",
    )