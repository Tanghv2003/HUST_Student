import reflex as rx

from HUST_Student.states.folder_state import FolderState


def answer_option_button(option: str):
    is_selected = FolderState.selected_answer == option
    is_correct = FolderState.correct_answer == option
    has_answered = FolderState.selected_answer != ""

    return rx.box(
        rx.hstack(
            rx.text(
                option,
                font_size="1rem",
                font_weight=rx.cond(is_correct & has_answered, "700", "500"),
                color=rx.cond(
                    has_answered,
                    rx.cond(is_correct, "#15803D",
                            rx.cond(is_selected, "#B91C1C", "#9CA3AF")),
                    "#111827",
                ),
                flex="1",
            ),
            rx.cond(
                has_answered & is_correct,
                rx.icon("check", size=18, color="#16A34A"),
                rx.cond(
                    has_answered & is_selected & ~is_correct,
                    rx.icon("x", size=18, color="#DC2626"),
                    rx.box(),
                ),
            ),
            align="center", width="100%",
        ),
        width="100%",
        padding="1.1rem 1.25rem",
        border=rx.cond(
            has_answered & is_correct, "2px solid #16A34A",
            rx.cond(has_answered & is_selected & ~is_correct, "2px solid #DC2626", "1.5px solid #E5E7EB"),
        ),
        border_radius="14px",
        bg=rx.cond(
            has_answered,
            rx.cond(is_correct, "#DCFCE7", rx.cond(is_selected, "#FECACA", "white")),
            "white",
        ),
        cursor=rx.cond(has_answered, "default", "pointer"),
        on_click=lambda: FolderState.set_selected_answer(option),
        _hover=rx.cond(has_answered, {}, {"bg": "#F5F3FF", "border_color": "#4F46E5"}),
        transition="all 0.15s ease",
    )


def trac_nghiem_section():
    question_label = rx.cond(FolderState.answer_language == "Foreign", "Native", "Foreign")

    return rx.vstack(
        rx.hstack(
            rx.text(question_label, font_size="0.85rem", font_weight="600", color="#6B7280",
                    text_transform="uppercase", letter_spacing="0.05em"),
            rx.spacer(),
            rx.text(FolderState.current_test_index + 1, " / ", FolderState.test_question_count,
                    font_weight="700", color="#6B7280", font_size="0.9rem"),
            width="100%", align="center",
        ),
        rx.progress(
            value=rx.cond(
                FolderState.test_question_count > 0,
                ((FolderState.current_test_index + 1) * 100) // FolderState.test_question_count,
                0,
            ),
            max=100, width="100%", color_scheme="indigo", size="1",
        ),
        rx.box(
            rx.text(FolderState.current_question_display,
                    font_size="1.4rem", font_weight="600", color="#111827",
                    text_align="left", line_height="1.4"),
            padding="1.5rem", border="1px solid #E5E7EB", border_radius="16px",
            bg="#F8FAFC", width="100%", min_height="100px",
        ),
        rx.text("Chọn đáp án đúng", font_size="0.82rem", color="#6B7280", font_weight="500"),
        rx.grid(
            rx.foreach(FolderState.current_options, answer_option_button),
            template_columns="repeat(2, minmax(0, 1fr))",
            gap="3", width="100%",
        ),
        rx.vstack(
            rx.text(
                "Bạn không biết?",
                color="#4F46E5", font_weight="600", font_size="0.9rem", cursor="pointer",
                align_self="center", on_click=FolderState.show_hint,
                _hover={"text_decoration": "underline"},
            ),
            rx.cond(
                FolderState.hint_text != "",
                rx.text(FolderState.hint_text, font_size="0.85rem", color="#6B7280", text_align="center"),
            ),
            spacing="1", align="center",
        ),
        rx.hstack(
            rx.button(
                "Đóng", on_click=FolderState.close_test,
                bg="#F3F4F6", color="#374151", border_radius="12px",
                padding="0.6rem 1.2rem", _hover={"bg": "#E5E7EB"},
            ),
            rx.spacer(),
            rx.button(
                "Tiếp theo →", on_click=FolderState.next_test_question,
                bg=rx.cond(FolderState.selected_answer != "", "#4F46E5", "#C7D2FE"),
                color="white", border_radius="12px", padding="0.6rem 1.2rem",
                _hover={"bg": "#4338CA"},
                cursor=rx.cond(FolderState.selected_answer != "", "pointer", "not-allowed"),
            ),
            width="100%", align="center",
        ),
        spacing="4", width="100%",
    )
