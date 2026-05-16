import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.folder_state import FolderState


def studyset_card(title, terms):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon("book-open", size=16, color=T.PRIMARY),
                    bg=T.PRIMARY_TINT,
                    border_radius=T.RADIUS_MD,
                    padding="0.5rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.spacer(),
                rx.box(
                    rx.text(f"{terms}", font_size="0.72rem", color=T.TEXT_MUTED, font_weight="600"),
                    rx.text(" từ", font_size="0.72rem", color=T.TEXT_MUTED),
                    display="flex",
                    align_items="center",
                    bg=T.BORDER_LIGHT,
                    padding="0.2rem 0.55rem",
                    border_radius="999px",
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                title,
                font_size="0.975rem",
                font_weight="700",
                color=T.TEXT_PRIMARY,
                no_of_lines=2,
                line_height="1.35",
            ),
            rx.hstack(
                rx.icon("play", size=13, color=T.PRIMARY),
                rx.text("Bắt đầu học", font_size="0.78rem", color=T.PRIMARY, font_weight="600"),
                spacing="1",
                align="center",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="1rem 1.1rem",
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        bg=T.SURFACE,
        cursor="pointer",
        box_shadow=T.SHADOW_CARD,
        transition="all 0.12s ease",
        on_click=lambda: FolderState.select_set(title),
        _hover={
            "border_color": T.PRIMARY,
            "box_shadow": T.SHADOW_CARD_HOVER,
            "transform": "translateY(-1px)",
        },
    )