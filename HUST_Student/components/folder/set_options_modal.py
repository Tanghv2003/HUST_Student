import reflex as rx

from HUST_Student.components.ui.modal import modal_close_btn, option_button
from HUST_Student.states.folder_state import FolderState


def set_options_modal():
    return rx.cond(
        FolderState.show_set_options,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(FolderState.selected_set.title, font_size="1.5rem", font_weight="700"),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_set_options),
                        width="100%", align="center",
                    ),
                    rx.divider(),
                    rx.grid(
                        option_button("bookmark", "Thẻ ghi nhớ", on_click=FolderState.start_flashcards),
                        option_button("book-open", "Học", on_click=FolderState.start_learn_mode),
                        option_button("clipboard-check", "Kiểm tra", on_click=FolderState.open_test_options),
                        option_button("grid-3x3", "Khối hợp"),
                        option_button("zap", "Blast"),
                        option_button("shuffle", "Ghép thẻ"),
                        columns="3", spacing="4", width="100%",
                    ),
                    spacing="6", padding="2rem", width="100%",
                ),
                bg="white", border_radius="24px", width="600px", max_width="90%",
                box_shadow="0 20px 60px rgba(0,0,0,0.12)",
                on_click=rx.stop_propagation,
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg="rgba(0,0,0,0.35)", z_index="999", padding="1.5rem",
            on_click=FolderState.close_set_options,
        ),
        rx.box(),
    )
