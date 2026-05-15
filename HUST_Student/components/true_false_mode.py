import reflex as rx
from HUST_Student.states.folder_state import FolderState

def true_false_section():
    is_selected_true = FolderState.selected_answer == "Đúng"
    is_selected_false = FolderState.selected_answer == "Sai"
    is_correct_true = FolderState.correct_answer == "Đúng"
    is_correct_false = FolderState.correct_answer == "Sai"
    has_answered = FolderState.selected_answer != ""

    def option_button(label: str, is_selected, is_correct):
        return rx.button(
            rx.hstack(
                rx.text(label, font_size="1rem", font_weight=rx.cond(is_correct & has_answered, "700", "600"), flex="1"),
                rx.cond(
                    has_answered & is_correct,
                    rx.icon("check", size=18, color="#16A34A"),
                    rx.cond(
                        has_answered & is_selected & ~is_correct,
                        rx.icon("x", size=18, color="#DC2626"),
                        rx.box(),
                    ),
                ),
                align="center",
                width="100%",
            ),
            on_click=lambda: FolderState.set_selected_answer(label),
            width="100%",
            padding="1.1rem 1.25rem",
            border_radius="14px",
            bg=rx.cond(
                has_answered,
                rx.cond(is_correct, "#DCFCE7", rx.cond(is_selected, "#FECACA", "white")),
                "white",
            ),
            border=rx.cond(
                has_answered,
                rx.cond(is_correct, "2px solid #16A34A", rx.cond(is_selected, "2px solid #DC2626", "1.5px solid #E5E7EB")),
                rx.cond(is_selected, "2px solid #4F46E5", "1.5px solid #E5E7EB"),
            ),
            cursor=rx.cond(has_answered, "default", "pointer"),
            _hover=rx.cond(has_answered, {}, {"bg": "#F5F3FF", "border_color": "#4F46E5"}),
        )

    return rx.vstack(
        rx.hstack(
            rx.text("Đúng / Sai", font_size="1rem", font_weight="700"),
            rx.spacer(),
            rx.text(FolderState.current_test_index + 1, "/", FolderState.test_question_count, color="#6B7280"),
            width="100%",
        ),
        rx.divider(),
        rx.hstack(
            rx.vstack(
                rx.text("Định nghĩa", color="#6B7280", font_weight="600"),
                rx.box(rx.text(FolderState.current_question_display, font_size="1.4rem", font_weight="700"), padding="1rem", bg="#F8FAFC", border_radius="12px", border="1px solid #E5E7EB", width="100%"),
                flex="1",
            ),
            rx.box(width="1px", bg="#E5E7EB"),
            rx.vstack(
                rx.text("Thuật ngữ", color="#6B7280", font_weight="600", align_self="flex-end"),
                rx.box(rx.text(FolderState.dung_sai_candidate, font_size="1.3rem", font_weight="700", text_align="right"), padding="1rem", bg="#F8FAFC", border_radius="12px", border="1px solid #E5E7EB", width="100%", align_self="flex-end"),
                flex="1",
            ),
            spacing="6",
            width="100%",
        ),
        rx.grid(
            option_button("Đúng", is_selected_true, is_correct_true),
            option_button("Sai", is_selected_false, is_correct_false),
            template_columns="repeat(2, minmax(0, 1fr))",
            gap="4",
            width="100%",
        ),
        rx.hstack(
            rx.text("Bạn không biết?", color="#4F46E5", font_weight="600", cursor="pointer", on_click=lambda: FolderState.set_selected_answer(FolderState.correct_answer), _hover={"text_decoration": "underline"}),
            rx.spacer(),
            rx.button("Tiếp", on_click=FolderState.next_test_question, bg=rx.cond(FolderState.selected_answer != "", "#4F46E5", "#C7D2FE"), color="white", border_radius="999px", padding="0.6rem 1.2rem", cursor=rx.cond(FolderState.selected_answer != "", "pointer", "not-allowed")),
        ),
        spacing="4",
        width="100%",
    )