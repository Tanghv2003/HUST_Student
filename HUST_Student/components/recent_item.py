import reflex as rx


def recent_item(
    title: str,
    subtitle: str,
):

    return rx.hstack(

        rx.box(
            rx.icon(
                "book",
                size=20,
            ),

            bg="#E0F2FE",

            border_radius="12px",

            padding="0.8rem",
        ),

        rx.vstack(

            rx.text(
                title,
                font_weight="600",
            ),

            rx.text(
                subtitle,
                color="#6B7280",
                font_size="0.9rem",
            ),

            spacing="1",
            align="start",
        ),

        rx.spacer(),

        rx.icon(
            "ellipsis_vertical",
            size=18,
        ),

        width="100%",

        padding="1rem",

        bg="white",

        border="1px solid #E5E7EB",

        border_radius="18px",

        align="center",
    )