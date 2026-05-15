import reflex as rx

from HUST_Student.states.folder_state import FolderState


def studyset_card(title, terms):
    return rx.box(
        rx.vstack(
            rx.text(title, font_size="1.3rem", font_weight="700"),
            rx.text(f"{terms} thuật ngữ", color="#6B7280"),
            align="start", spacing="1",
        ),
        padding="1.2rem",
        border="1px solid #E5E7EB",
        border_radius="16px",
        bg="white",
        width="100%",
        cursor="pointer",
        on_click=lambda: FolderState.select_set(title),
        _hover={"bg": "#F9FAFB", "border_color": "#4F46E5"},
    )
