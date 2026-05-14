import reflex as rx


def class_card(
    title: str,
    students: str,
    color: str,
):

    return rx.box(

        rx.vstack(

            rx.hstack(

                rx.box(
                    width="14px",
                    height="14px",
                    border_radius="999px",
                    bg=color,
                ),

                rx.text(
                    title,
                    font_weight="700",
                    font_size="1.2rem",
                ),

                spacing="3",
                align="center",
            ),

            rx.text(
                students,
                color="#6B7280",
            ),

            rx.button(
                "Vào lớp",
                bg="#4F46E5",
                color="white",
                border_radius="12px",
            ),

            spacing="4",
            align="start",
        ),

        bg="white",

        border="1px solid #E5E7EB",

        border_radius="20px",

        padding="1.5rem",

        width="320px",
    )


def classes_page():

    return rx.vstack(

        rx.hstack(

            rx.text(
                "Lớp học của tôi",
                font_size="2.5rem",
                font_weight="700",
            ),

            rx.spacer(),

            rx.button(
                "+ Tạo lớp học",
                bg="#4F46E5",
                color="white",
                border_radius="12px",
            ),

            width="100%",
        ),

        rx.grid(

            class_card(
                "Tiếng Nhật N5",
                "42 học viên",
                "#22C55E",
            ),

            class_card(
                "Toeic 700+",
                "28 học viên",
                "#3B82F6",
            ),

            class_card(
                "Kanji N4",
                "35 học viên",
                "#EC4899",
            ),

            class_card(
                "Ngữ pháp N3",
                "19 học viên",
                "#F59E0B",
            ),

            columns="2",

            spacing="6",

            width="100%",
        ),

        spacing="7",

        width="100%",
    )