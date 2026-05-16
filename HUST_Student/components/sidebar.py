import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.navigation_state import NavigationState


def sidebar_item(icon: str, text: str, active, on_click):
    return rx.hstack(
        rx.icon(icon, size=17, color=rx.cond(active, T.PRIMARY, T.TEXT_SECONDARY)),
        rx.text(
            text,
            font_weight=rx.cond(active, "600", "500"),
            font_size="0.875rem",
            color=rx.cond(active, T.PRIMARY, T.TEXT_PRIMARY),
        ),
        spacing="3",
        align="center",
        width="100%",
        padding="0.6rem 0.9rem",
        border_radius=T.RADIUS_MD,
        bg=rx.cond(active, T.PRIMARY_TINT, "transparent"),
        cursor="pointer",
        transition="background 0.12s ease",
        _hover={"bg": T.BORDER_LIGHT},
        on_click=on_click,
    )


def _library_tree_section():
    """Section cây thư mục trong sidebar — chỉ hiện khi đang ở library/folder."""
    from HUST_Student.components.folder_tree import folder_node
    from HUST_Student.services.folder_service import load_folders

    try:
        data = load_folders()
    except Exception:
        data = {}

    return rx.cond(
        (NavigationState.current_page == "library")
        | (NavigationState.current_page == "folder_detail"),
        rx.vstack(
            rx.box(height="1px", width="100%", bg=T.BORDER_LIGHT, margin_y="0.25rem"),
            rx.text(
                "THƯ MỤC",
                font_size="0.65rem",
                font_weight="700",
                color=T.TEXT_MUTED,
                letter_spacing="0.1em",
                padding_x="0.9rem",
                padding_y="0.25rem",
            ),
            rx.box(
                rx.vstack(
                    *[
                        folder_node(name, children)
                        for name, children in data.items()
                    ],
                    spacing="0",
                    width="100%",
                ),
                width="100%",
                overflow_y="auto",
                max_height="calc(100vh - 320px)",
            ),
            spacing="0",
            width="100%",
            align="start",
        ),
        rx.box(),
    )


def sidebar():
    return rx.vstack(
        # Logo
        rx.hstack(
            rx.text(
                "Q",
                color=T.PRIMARY,
                font_size="1.75rem",
                font_weight="800",
                font_family="system-ui, -apple-system, sans-serif",
                letter_spacing="-0.02em",
            ),
            rx.text(
                "HUST",
                color=T.TEXT_PRIMARY,
                font_size="1rem",
                font_weight="700",
                letter_spacing="0.02em",
            ),
            spacing="2",
            align="center",
            padding_bottom="0.75rem",
        ),

        # Nav items
        rx.vstack(
            sidebar_item(
                "house",
                "Trang chủ",
                NavigationState.current_page == "home",
                NavigationState.go_home,
            ),
            sidebar_item(
                "folder",
                "Thư viện",
                (NavigationState.current_page == "library")
                | (NavigationState.current_page == "folder_detail"),
                NavigationState.go_library,
            ),
            sidebar_item(
                "message-circle",
                "Hội thoại",
                NavigationState.current_page == "conversation",
                NavigationState.go_conversation,
            ),
            sidebar_item(
                "graduation-cap",
                "Lớp học",
                NavigationState.current_page == "classes",
                NavigationState.go_classes,
            ),
            spacing="0",
            width="100%",
        ),

        # Folder tree (chỉ hiện trong library)
        _library_tree_section(),

        rx.spacer(),

        # Bottom: upgrade badge nhỏ
        rx.box(
            rx.vstack(
                rx.text("Nâng cấp Pro", font_size="0.8rem", font_weight="700", color=T.UPGRADE_TEXT),
                rx.text("Dùng thử 7 ngày miễn phí", font_size="0.72rem", color=T.TEXT_SECONDARY),
                spacing="0",
                align="start",
            ),
            bg=T.UPGRADE_YELLOW,
            border_radius=T.RADIUS_MD,
            padding="0.75rem 1rem",
            width="100%",
            cursor="pointer",
            _hover={"filter": "brightness(0.97)"},
        ),

        width="260px",
        height="100vh",
        padding="1.25rem 0.875rem",
        bg=T.SURFACE,
        border_right=f"1px solid {T.BORDER_LIGHT}",
        position="fixed",
        left="0",
        top="0",
        z_index="40",
        box_shadow="2px 0 12px rgba(46, 56, 86, 0.04)",
        overflow="hidden",
        spacing="1",
        align="start",
    )