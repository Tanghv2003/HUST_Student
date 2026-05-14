import reflex as rx


def topbar():

    return rx.hstack(

        rx.input(
            placeholder="Tìm kiếm hướng dẫn học",
            width="650px",
            bg="#F3F4F6",
            border="none",
            border_radius="16px",
            size="3",
        ),

        rx.spacer(),

        rx.button(
            "+",
            bg="#4F46E5",
            color="white",
            border_radius="999px",
            width="48px",
            height="48px",
            font_size="1.5rem",
        ),

        rx.button(
            "Nâng cấp: dùng thử miễn phí 7 ngày",
            bg="#FACC15",
            color="black",
            border_radius="999px",
            padding_x="1.5rem",
        ),

        rx.avatar(
            name="No",
            size="4",
        ),

        width="100%",
        align="center",
    )