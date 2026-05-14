import reflex as rx


def sidebar_item(icon: str, text: str, active=False):

    return rx.hstack(

        rx.icon(
            icon,
            size=20,
        ),

        rx.text(
            text,
            font_weight="600" if active else "500",
        ),

        spacing="3",

        align="center",

        width="100%",

        padding="0.9rem 1rem",

        border_radius="14px",

        bg="#EEF2FF" if active else "transparent",

        color="#4F46E5" if active else "#374151",

        cursor="pointer",

        _hover={
            "bg": "#F3F4F6",
        },
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
                True,
            ),

            sidebar_item(
                "folder",
                "Thư viện của bạn",
            ),

            sidebar_item(
                "users",
                "Nhóm học",
            ),

            sidebar_item(
                "bell",
                "Thông báo",
            ),

            spacing="2",

            width="100%",
        ),

        rx.divider(),

        rx.vstack(

            rx.text(
                "BỘ SƯU TẬP CỦA BẠN",
                font_size="0.8rem",
                font_weight="700",
                color="#6B7280",
            ),

            sidebar_item(
                "folder",
                "Tính từ N4",
            ),

            sidebar_item(
                "folder",
                "Kanji N5",
            ),

            sidebar_item(
                "folder",
                "Toeic Vocabulary",
            ),

            sidebar_item(
                "folder",
                "Ngữ pháp N4",
            ),

            spacing="2",

            width="100%",
            align="start",
        ),

        rx.spacer(),

        rx.box(

            rx.vstack(

                rx.text(
                    "Quizlet Plus",
                    font_weight="700",
                    font_size="1.1rem",
                ),

                rx.text(
                    "Học nhanh hơn với AI và flashcard.",
                    color="#6B7280",
                    font_size="0.9rem",
                ),

                rx.button(
                    "Dùng thử miễn phí",
                    width="100%",
                    bg="#4F46E5",
                    color="white",
                ),

                spacing="4",
                align="start",
            ),

            bg="#F5F3FF",

            border_radius="18px",

            padding="1rem",

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