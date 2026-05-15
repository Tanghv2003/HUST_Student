import reflex as rx

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
                    rx.text(
                        rx.cond(FolderState.selected_set, FolderState.selected_set.title, "Flashcards"),
                        font_size="1.5rem", font_weight="700",
                    ),
                    rx.text("Nhấp vào thẻ để lật", color="#6B7280", font_size="0.95rem"),
                    rx.box(
                        rx.text(current_word_text, font_size="2rem", font_weight="700",
                                text_align="center", padding="2rem"),
                        margin_top="1.5rem",
                        border="1px solid #E5E7EB", border_radius="24px",
                        bg="white", width="100%",
                        on_click=[rx.stop_propagation, FolderState.flip_card],
                        cursor="pointer", padding="2rem", min_height="220px",
                        display="flex", align_items="center", justify_content="center",
                    ),
                    rx.hstack(
                        rx.button(
                            "← Trước", on_click=FolderState.prev_word,
                            width="140px", bg="#FFFFFF", color="#111827",
                            border="1px solid #E5E7EB", border_radius="999px",
                            padding="0.9rem 1.2rem", _hover={"bg": "#F3F4F6"},
                        ),
                        rx.text(current_position, " / ", total_words, font_weight="700"),
                        rx.button(
                            "Tiếp →", on_click=FolderState.next_word,
                            width="140px", bg="#FFFFFF", color="#111827",
                            border="1px solid #E5E7EB", border_radius="999px",
                            padding="0.9rem 1.2rem", _hover={"bg": "#F3F4F6"},
                        ),
                        spacing="4", justify="center", align="center", width="100%",
                    ),
                    rx.button("Đóng", on_click=FolderState.close_flashcards,
                              bg="#F3F4F6", _hover={"bg": "#E5E7EB"}),
                    spacing="4", width="100%",
                ),
                bg="white", border_radius="24px", width="720px", max_width="97%",
                box_shadow="0 24px 80px rgba(0,0,0,0.16)", padding="2.5rem",
                on_click=rx.stop_propagation,
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg="rgba(0,0,0,0.35)", z_index="999", padding="1.5rem",
            on_click=FolderState.close_flashcards,
        ),
        rx.box(),
    )
