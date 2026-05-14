import reflex as rx

from HUST_Student.states.navigation_state import NavigationState


def sidebar_item(
    icon: str,
    text: str,
    active,
    on_click,
):

    return rx.hstack(

        rx.icon(
            icon,
            size=20,
        ),

        rx.text(
            text,

            font_weight=rx.cond(
                active,
                "600",
                "500",
            ),
        ),

        spacing="3",

        align="center",

        width="100%",

        padding="0.9rem 1rem",

        border_radius="14px",

        bg=rx.cond(
            active,
            "#EEF2FF",
            "transparent",
        ),

        color=rx.cond(
            active,
            "#4F46E5",
            "#374151",
        ),

        cursor="pointer",

        _hover={
            "bg": "#F3F4F6",
        },

        on_click=on_click,
    )


def sidebar():

    return rx.vstack(

        rx.hstack(

            rx.icon(
                "menu",
                size=28,
            ),

            rx.text(
                "Q",
                color="#4F46E5",
                font_size="2.2rem",
                font_weight="700",
            ),

            width="100%",
            justify="between",
            align="center",
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

            spacing="2",

            width="100%",
        ),

        width="280px",

        height="100vh",

        padding="1.5rem",

        bg="white",

        border_right="1px solid #E5E7EB",

        position="fixed",

        left="0",
        top="0",
    )