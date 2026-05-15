import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn, option_button
from HUST_Student.states.folder_state import FolderState


def set_options_modal():
    return rx.cond(
        FolderState.show_set_options,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            FolderState.selected_set.title,
                            font_size="1.4rem",
                            font_weight="800",
                            color=T.TEXT_PRIMARY,
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_set_options),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    rx.grid(
                        option_button("bookmark", "Thẻ ghi nhớ", on_click=FolderState.start_flashcards),
                        option_button("book-open", "Học", on_click=FolderState.start_learn_mode),
                        option_button("clipboard-check", "Kiểm tra", on_click=FolderState.open_test_options),
                        option_button("grid-3x3", "Khối hợp", on_click=FolderState.start_blocks),
                        option_button("zap", "Blast", on_click=FolderState.start_blast),
                        option_button("shuffle", "Ghép thẻ", on_click=FolderState.start_match),
                        columns="3",
                        spacing="4",
                        width="100%",
                    ),
                    spacing="6",
                    padding="2rem",
                    width="100%",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="600px",
                max_width="min(600px, calc(100vw - 2.5rem))",
                max_height=T.MODAL_CONTENT_MAX_HEIGHT,
                min_height="0",
                overflow_y="auto",
                overflow_x="hidden",
                border=f"1px solid {T.BORDER}",
                box_shadow=T.SHADOW_MODAL,
                on_click=rx.stop_propagation,
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            display="flex",
            align_items="center",
            justify_content="center",
            bg=T.OVERLAY_SCRIM,
            z_index="999",
            padding=T.MODAL_OVERLAY_PADDING,
            on_click=FolderState.close_set_options,
        ),
        rx.box(),
    )
