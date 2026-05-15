import reflex as rx

from HUST_Student.components.ui import theme as T


def modal_close_btn(on_click):
    return rx.button(
        rx.icon("x", size=18),
        on_click=on_click,
        bg="transparent",
        color=T.TEXT_SECONDARY,
        border_radius=T.RADIUS_SM,
        padding="0.4rem",
        _hover={"bg": T.BORDER_LIGHT},
    )


def option_button(icon: str, label: str, on_click=None):
    return rx.vstack(
        rx.icon(icon, size=32, color=T.PRIMARY),
        rx.text(label, font_size="0.9rem", font_weight="600", text_align="center", color=T.TEXT_PRIMARY),
        align="center",
        spacing="2",
        padding="1.5rem",
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_MD,
        bg=T.SURFACE,
        cursor="pointer",
        box_shadow=T.SHADOW_CARD,
        on_click=on_click,
        _hover={
            "bg": T.PRIMARY_TINT,
            "border_color": T.PRIMARY,
            "box_shadow": T.SHADOW_CARD_HOVER,
        },
    )
