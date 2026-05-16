import reflex as rx

from HUST_Student.components.ui import theme as T


def topbar():
    return rx.hstack(
        rx.box(
            rx.input(
                placeholder="Tìm kiếm...",
                width="100%",
                max_width="480px",
                bg=T.BORDER_LIGHT,
                border=f"1px solid {T.BORDER_LIGHT}",
                color=T.TEXT_PRIMARY,
                border_radius=T.RADIUS_PILL,
                height="40px",
                padding_x="1.1rem",
                size="2",
                _focus={
                    "border_color": T.PRIMARY,
                    "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                    "bg": T.SURFACE,
                },
            ),
            flex="1",
            max_width="520px",
        ),
        rx.spacer(),
        rx.button(
            "+ Tạo",
            bg=T.PRIMARY,
            color="white",
            border_radius=T.RADIUS_PILL,
            height="36px",
            padding_x="1rem",
            font_size="0.875rem",
            font_weight="600",
            _hover={"bg": T.PRIMARY_HOVER, "cursor": "pointer"},
        ),
        rx.avatar(
            name="User",
            size="2",
            color_scheme="indigo",
            variant="solid",
        ),
        width="100%",
        align="center",
        spacing="3",
        padding_bottom="0.5rem",
        border_bottom=f"1px solid {T.BORDER_LIGHT}",
        margin_bottom="0.5rem",
    )