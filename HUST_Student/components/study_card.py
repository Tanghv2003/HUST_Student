import reflex as rx


def study_card(title: str):

    return rx.box(

        rx.vstack(

            rx.text(
                title,
                font_size="2rem",
                font_weight="700",
            ),

            rx.progress(
                value=20,
                width="100%",
            ),

            rx.text(
                "20% completed",
                color="#6B7280",
            ),

            rx.button(
                "Continue",
                bg="#4F46E5",
                color="white",
                border_radius="999px",
            ),

            spacing="5",
            align="start",
        ),

        bg="white",

        border="1px solid #E5E7EB",

        border_radius="24px",

        padding="2rem",

        width="100%",

        min_height="260px",
    )