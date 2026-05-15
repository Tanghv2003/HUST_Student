import reflex as rx


def modal_close_btn(on_click):
    return rx.button(
        rx.icon("x", size=18),
        on_click=on_click,
        bg="transparent",
        color="#6B7280",
        border_radius="8px",
        padding="0.4rem",
        _hover={"bg": "#F3F4F6"},
    )


def option_button(icon: str, label: str, on_click=None):
    return rx.vstack(
        rx.icon(icon, size=32, color="#4F46E5"),
        rx.text(label, font_size="0.9rem", font_weight="600", text_align="center"),
        align="center",
        spacing="2",
        padding="1.5rem",
        border="1px solid #E5E7EB",
        border_radius="12px",
        bg="white",
        cursor="pointer",
        on_click=on_click,
        _hover={"bg": "#EEF2FF", "border_color": "#4F46E5"},
    )
