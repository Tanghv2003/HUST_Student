import reflex as rx

from HUST_Student.states.folder_state import FolderState


def essay_section():
    return rx.vstack(
        rx.hstack(
            rx.text(
                rx.cond(FolderState.answer_language == "Foreign", "Native", "Foreign"),
                font_size="0.85rem", font_weight="600", color="#6B7280",
                text_transform="uppercase", letter_spacing="0.05em",
            ),
            rx.spacer(),
            rx.text(
                FolderState.current_test_index + 1, " / ",
                FolderState.test_question_count,
                font_weight="700", color="#6B7280", font_size="0.9rem",
            ),
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
                    font_size="1.3rem", font_weight="600",
                    color="#111827", text_align="left"),
            padding="1rem", border="1px solid #E5E7EB",
            border_radius="12px", bg="#F8FAFC",
            width="100%", min_height="100px",
        ),
        rx.box(
            rx.text("Đáp án của bạn", font_weight="600", color="#6B7280"),
            rx.input(
                value=FolderState.written_answer,
                on_change=FolderState.set_written_answer,
                placeholder="Nhập đáp án",
                width="100%", height="140px",
                bg="#F8FAFC", border="none", border_radius="16px",
                padding="1.25rem", font_size="1rem",
            ),
            spacing="3", width="100%",
        ),
        rx.cond(
            FolderState.check_feedback != "",
            rx.text(
                FolderState.check_feedback,
                font_size="0.9rem",
                color=rx.cond(FolderState.check_feedback.contains("✅"), "#16A34A", "#DC2626"),
                font_weight="500", text_align="center",
            ),
            rx.box(),
        ),
        rx.hstack(
            rx.button(
                "Đóng", on_click=FolderState.close_test,
                bg="#F3F4F6", color="#374151", border_radius="12px",
                padding="0.6rem 1.2rem", _hover={"bg": "#E5E7EB"},
            ),
            rx.button(
                "Kiểm tra", on_click=FolderState.check_current_answer,
                bg="#F59E0B", color="white", border_radius="12px",
                padding="0.6rem 1.2rem", _hover={"bg": "#D97706"},
            ),
            rx.spacer(),
            rx.button(
                "Tiếp",
                on_click=FolderState.next_test_question,
                bg=rx.cond(FolderState.written_answer != "", "#4F46E5", "#C7D2FE"),
                color="white", border_radius="12px",
                padding="0.6rem 1.2rem", _hover={"bg": "#4338CA"},
                cursor=rx.cond(FolderState.written_answer != "", "pointer", "not-allowed"),
            ),
            width="100%", align="center", spacing="3",
        ),
        spacing="4", width="100%",
    )
