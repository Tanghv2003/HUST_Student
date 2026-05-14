import reflex as rx

from HUST_Student.states.folder_state import FolderState
from HUST_Student.states.navigation_state import NavigationState


def option_button(icon: str, label: str, on_click=None):
    """Create an option button for study set actions"""
    return rx.vstack(
        rx.icon(
            icon,
            size=32,
            color="#4F46E5",
        ),
        rx.text(
            label,
            font_size="0.9rem",
            font_weight="600",
            text_align="center",
        ),
        align="center",
        spacing="2",
        padding="1.5rem",
        border="1px solid #E5E7EB",
        border_radius="12px",
        bg="white",
        cursor="pointer",
        on_click=on_click,
        _hover={
            "bg": "#EEF2FF",
            "border_color": "#4F46E5",
        },
    )


def set_options_modal():
    """Modal showing study set options"""
    return rx.cond(
        FolderState.show_set_options,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            FolderState.selected_set.title,
                            font_size="1.5rem",
                            font_weight="700",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon("x", size=20),
                            on_click=FolderState.close_set_options,
                            bg="transparent",
                            _hover={"bg": "#F3F4F6"},
                        ),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    rx.grid(
                        option_button("bookmark", "Thẻ ghi nhớ", on_click=FolderState.start_flashcards),
                        option_button("book-open", "Học"),
                        option_button("clipboard-check", "Kiểm tra"),
                        option_button("grid-3x3", "Khối hợp"),
                        option_button("zap", "Blast"),
                        option_button("shuffle", "Ghép thẻ"),
                        columns="3",
                        spacing="4",
                        width="100%",
                    ),
                    spacing="6",
                    padding="2rem",
                    width="100%",
                ),
                bg="white",
                border_radius="24px",
                width="600px",
                max_width="90%",
                box_shadow="0 20px 60px rgba(0,0,0,0.12)",
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
            bg="rgba(0,0,0,0.35)",
            z_index="999",
            padding="1.5rem",
            on_click=FolderState.close_set_options,
        ),
        rx.box(),
    )


def studyset_card(title, terms):

    return rx.box(

        rx.vstack(

            rx.text(
                title,
                font_size="1.3rem",
                font_weight="700",
            ),

            rx.text(
                f"{terms} thuật ngữ",
                color="#6B7280",
            ),

            align="start",
            spacing="1",
        ),

        padding="1.2rem",

        border="1px solid #E5E7EB",

        border_radius="16px",

        bg="white",

        width="100%",

        cursor="pointer",

        on_click=lambda: FolderState.select_set(title),

        _hover={
            "bg": "#F9FAFB",
            "border_color": "#4F46E5",
        },
    )


def flashcard_overlay():
    current_word = rx.cond(
        FolderState.selected_set,
        FolderState.selected_set.words[FolderState.current_word_index],
        None,
    )

    return rx.cond(
        FolderState.show_flashcards,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.text(
                        rx.cond(
                            FolderState.selected_set,
                            FolderState.selected_set.title,
                            "Flashcards",
                        ),
                        font_size="1.5rem",
                        font_weight="700",
                    ),
                    rx.text(
                        "Nhấn chuột phải để lật thẻ",
                        color="#6B7280",
                        font_size="0.95rem",
                    ),
                    rx.box(
                        rx.text(
                            rx.cond(
                                FolderState.selected_set,
                                rx.cond(
                                    FolderState.is_flipped,
                                    FolderState.selected_set.words[FolderState.current_word_index].back,
                                    FolderState.selected_set.words[FolderState.current_word_index].front,
                                ),
                                "",
                            ),
                            font_size="2rem",
                            font_weight="700",
                            text_align="center",
                            padding="2rem",
                        ),
                        margin_top="1.5rem",
                        border="1px solid #E5E7EB",
                        border_radius="24px",
                        bg="white",
                        width="100%",
                        on_context_menu=[rx.prevent_default, FolderState.flip_card],
                        on_click=rx.stop_propagation,
                        padding="2rem",
                        min_height="220px",
                        align="center",
                        justify="center",
                    ),
                    rx.hstack(
                        rx.button(
                            "Back",
                            on_click=FolderState.prev_word,
                            width="120px",
                            bg="#E5E7EB",
                            _hover={"bg": "#D1D5DB"},
                        ),
                        rx.text(
                            rx.cond(
                                FolderState.selected_set,
                                FolderState.current_word_index + 1,
                                "0",
                            ),
                            font_weight="600",
                        ),
                        rx.button(
                            "Next",
                            on_click=FolderState.next_word,
                            width="120px",
                            bg="#E5E7EB",
                            _hover={"bg": "#D1D5DB"},
                        ),
                        spacing="4",
                        justify="center",
                        align="center",
                        width="100%",
                    ),
                    rx.button(
                        "Đóng",
                        on_click=FolderState.close_flashcards,
                        bg="#F3F4F6",
                        _hover={"bg": "#E5E7EB"},
                    ),
                    spacing="4",
                    width="100%",
                ),
                bg="white",
                border_radius="24px",
                width="640px",
                max_width="95%",
                box_shadow="0 24px 80px rgba(0,0,0,0.16)",
                padding="2rem",
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
            bg="rgba(0,0,0,0.35)",
            z_index="999",
            padding="1.5rem",
            on_click=FolderState.close_flashcards,
        ),
        rx.box(),
    )


def folder_detail_page():

    return rx.vstack(

        set_options_modal(),

        flashcard_overlay(),

        rx.text(
            NavigationState.current_folder,
            font_size="2.5rem",
            font_weight="700",
        ),

        rx.vstack(

            rx.foreach(
                FolderState.current_sets,
                lambda item: studyset_card(
                    item.title,
                    item.terms,
                ),
            ),

            spacing="4",

            width="100%",
        ),

        width="100%",
        spacing="6",
    )