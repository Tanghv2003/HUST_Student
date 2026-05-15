import reflex as rx

from HUST_Student.components.ui import theme as T


def topbar():
    return rx.hstack(
        rx.box(
            rx.input(
                placeholder="Tìm kiếm hướng dẫn học",
                width="100%",
                max_width="640px",
                bg=T.BORDER_LIGHT,
                border=f"1px solid {T.BORDER_LIGHT}",
                color=T.TEXT_PRIMARY,
                border_radius=T.RADIUS_PILL,
                height="48px",
                padding_x="1.25rem",
                size="3",
                _focus={
                    "border_color": T.PRIMARY,
                    "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                    "bg": T.SURFACE,
                },
            ),
            flex="1",
            max_width="720px",
        ),
        rx.spacer(),
        rx.button(
            "+",
            bg=T.PRIMARY,
            color="white",
            border_radius=T.RADIUS_PILL,
            width="48px",
            height="48px",
            font_size="1.35rem",
            font_weight="500",
            line_height="1",
            _hover={"bg": T.PRIMARY_HOVER, "cursor": "pointer"},
        ),
        rx.button(
            "Nâng cấp: dùng thử miễn phí 7 ngày",
            bg=T.UPGRADE_YELLOW,
            color=T.UPGRADE_TEXT,
            font_weight="700",
            font_size="0.875rem",
            border_radius=T.RADIUS_PILL,
            padding_x="1.25rem",
            height="44px",
            border="none",
            _hover={"filter": "brightness(0.97)", "cursor": "pointer"},
        ),
        rx.avatar(
            name="No",
            size="4",
            color_scheme="gray",
            variant="solid",
        ),
        width="100%",
        align="center",
        spacing="4",
        padding_bottom="0.25rem",
    )
