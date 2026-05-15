import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.navigation_state import NavigationState


def sidebar_item(
    icon: str,
    text: str,
    active,
    on_click,
):
    return rx.hstack(
        rx.icon(icon, size=20, color=rx.cond(active, T.PRIMARY, T.TEXT_SECONDARY)),
        rx.text(
            text,
            font_weight=rx.cond(active, "600", "500"),
            font_size="0.95rem",
            color=rx.cond(active, T.PRIMARY, T.TEXT_PRIMARY),
        ),
        spacing="3",
        align="center",
        width="100%",
        padding="0.75rem 1rem",
        border_radius=T.RADIUS_MD,
        bg=rx.cond(active, T.PRIMARY_TINT, "transparent"),
        cursor="pointer",
        transition="background 0.15s ease",
        _hover={
            "bg": T.BORDER_LIGHT,
        },
        on_click=on_click,
    )


def sidebar():
    return rx.vstack(
        rx.hstack(
            rx.icon("menu", size=26, color=T.TEXT_PRIMARY, cursor="pointer"),
            rx.text(
                "Q",
                color=T.PRIMARY,
                font_size="2rem",
                font_weight="800",
                font_family="system-ui, -apple-system, sans-serif",
                letter_spacing="-0.02em",
            ),
            width="100%",
            justify="between",
            align="center",
            padding_bottom="0.5rem",
        ),
        rx.vstack(
            sidebar_item(
                "house",
                "Trang chủ",
                NavigationState.current_page == "home",
                NavigationState.go_home,
            ),
            sidebar_item(
                "folder",
                "Thư viện của bạn",
                NavigationState.current_page == "library",
                NavigationState.go_library,
            ),
            sidebar_item(
                "graduation_cap",
                "Lớp học của tôi",
                NavigationState.current_page == "classes",
                NavigationState.go_classes,
            ),
            spacing="1",
            width="100%",
        ),
        width="280px",
        height="100vh",
        padding="1.25rem 1rem",
        bg=T.SURFACE,
        border_right=f"1px solid {T.BORDER_LIGHT}",
        position="fixed",
        left="0",
        top="0",
        z_index="40",
        box_shadow="2px 0 12px rgba(46, 56, 86, 0.04)",
    )
