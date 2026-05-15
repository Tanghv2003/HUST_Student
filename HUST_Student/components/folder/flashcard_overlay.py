import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.folder_state import FolderState


def flashcard_overlay():
    current_word = rx.cond(
        FolderState.selected_set,
        FolderState.selected_set.words[FolderState.current_word_index],
        None,
    )
    current_word_text = rx.cond(
        current_word,
        rx.cond(FolderState.is_flipped, current_word.back, current_word.front),
        "",
    )
    current_position = rx.cond(FolderState.selected_set, FolderState.current_word_index + 1, 0)
    total_words = rx.cond(FolderState.selected_set, FolderState.selected_set.words.length(), 0)

    return rx.cond(
        FolderState.show_flashcards,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.vstack(
                        rx.text(
                            rx.cond(FolderState.selected_set, FolderState.selected_set.title, "Flashcards"),
                            font_size="1.35rem",
                            font_weight="800",
                            color=T.TEXT_PRIMARY,
                        ),
                        rx.text(
                            "Nhấp vào thẻ để lật",
                            color=T.TEXT_SECONDARY,
                            font_size="0.9rem",
                        ),
                        spacing="1",
                        align="start",
                        width="100%",
                    ),
                    rx.box(
                        rx.text(
                            current_word_text,
                            font_size="2rem",
                            font_weight="700",
                            color=T.TEXT_PRIMARY,
                            text_align="center",
                            padding="2rem",
                        ),
                        margin_top="0.5rem",
                        border=f"1px solid {T.BORDER}",
                        border_radius=T.RADIUS_XL,
                        bg=T.SURFACE,
                        width="100%",
                        min_height="240px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        on_click=[rx.stop_propagation, FolderState.flip_card],
                        cursor="pointer",
                        box_shadow=T.SHADOW_CARD,
                        transition="transform 0.15s ease",
                        _hover={"border_color": T.PRIMARY},
                    ),
                    rx.hstack(
                        rx.button(
                            "← Trước",
                            on_click=FolderState.prev_word,
                            width="140px",
                            bg=T.SURFACE,
                            color=T.TEXT_PRIMARY,
                            border=f"1px solid {T.BORDER}",
                            border_radius=T.RADIUS_PILL,
                            padding="0.85rem 1.2rem",
                            font_weight="600",
                            _hover={"bg": T.BORDER_LIGHT},
                        ),
                        rx.text(
                            current_position,
                            " / ",
                            total_words,
                            font_weight="700",
                            color=T.TEXT_SECONDARY,
                            min_width="72px",
                            text_align="center",
                        ),
                        rx.button(
                            "Tiếp →",
                            on_click=FolderState.next_word,
                            width="140px",
                            bg=T.SURFACE,
                            color=T.TEXT_PRIMARY,
                            border=f"1px solid {T.BORDER}",
                            border_radius=T.RADIUS_PILL,
                            padding="0.85rem 1.2rem",
                            font_weight="600",
                            _hover={"bg": T.BORDER_LIGHT},
                        ),
                        spacing="4",
                        justify="center",
                        align="center",
                        width="100%",
                    ),
                    rx.button(
                        "Đóng",
                        on_click=FolderState.close_flashcards,
                        bg=T.BORDER_LIGHT,
                        color=T.TEXT_PRIMARY,
                        border_radius=T.RADIUS_MD,
                        font_weight="600",
                        _hover={"bg": T.BORDER},
                    ),
                    spacing="5",
                    width="100%",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="720px",
                max_width="min(720px, calc(100vw - 2.5rem))",
                max_height=T.MODAL_CONTENT_MAX_HEIGHT,
                min_height="0",
                overflow_y="auto",
                overflow_x="hidden",
                border=f"1px solid {T.BORDER}",
                box_shadow=T.SHADOW_MODAL,
                padding="2.25rem",
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
            on_click=FolderState.close_flashcards,
        ),
        rx.box(),
    )
