import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.folder_state import FolderState


def studyset_card(title, terms):
    return rx.box(
        rx.vstack(
            rx.text(title, font_size="1.2rem", font_weight="700", color=T.TEXT_PRIMARY),
            rx.text(f"{terms} thuật ngữ", color=T.TEXT_SECONDARY, font_size="0.9rem"),
            align="start",
            spacing="1",
        ),
        padding="1.35rem",
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        bg=T.SURFACE,
        width="100%",
        cursor="pointer",
        box_shadow=T.SHADOW_CARD,
        transition="box-shadow 0.15s ease, border-color 0.15s ease",
        on_click=lambda: FolderState.select_set(title),
        _hover={
            "bg": T.SURFACE,
            "border_color": T.PRIMARY,
            "box_shadow": T.SHADOW_CARD_HOVER,
        },
    )
