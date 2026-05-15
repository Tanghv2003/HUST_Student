import reflex as rx

from HUST_Student.components.ui import theme as T
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
                rx.text(
                    label,
                    font_size="1rem",
                    font_weight=rx.cond(is_correct & has_answered, "700", "600"),
                    flex="1",
                    color=T.TEXT_PRIMARY,
                ),
                rx.cond(
                    has_answered & is_correct,
                    rx.icon("check", size=18, color=T.SUCCESS),
                    rx.cond(
                        has_answered & is_selected & ~is_correct,
                        rx.icon("x", size=18, color=T.DANGER),
                        rx.box(),
                    ),
                ),
                align="center",
                width="100%",
            ),
            on_click=lambda: FolderState.set_selected_answer(label),
            width="100%",
            padding="1.1rem 1.25rem",
            border_radius=T.RADIUS_MD,
            bg=rx.cond(
                has_answered,
                rx.cond(is_correct, T.SUCCESS_BG, rx.cond(is_selected, T.DANGER_BG, T.SURFACE)),
                T.SURFACE,
            ),
            border=rx.cond(
                has_answered,
                rx.cond(
                    is_correct,
                    f"2px solid {T.SUCCESS}",
                    rx.cond(is_selected, f"2px solid {T.DANGER}", f"1.5px solid {T.BORDER}"),
                ),
                rx.cond(is_selected, f"2px solid {T.PRIMARY}", f"1.5px solid {T.BORDER}"),
            ),
            cursor=rx.cond(has_answered, "default", "pointer"),
            _hover=rx.cond(has_answered, {}, {"bg": T.PRIMARY_TINT, "border_color": T.PRIMARY}),
        )

    return rx.vstack(
        rx.hstack(
            rx.text("Đúng / Sai", font_size="1rem", font_weight="800", color=T.TEXT_PRIMARY),
            rx.spacer(),
            rx.text(
                FolderState.current_test_index + 1,
                "/",
                FolderState.test_question_count,
                color=T.TEXT_SECONDARY,
                font_weight="700",
            ),
            width="100%",
        ),
        rx.divider(),
        rx.hstack(
            rx.vstack(
                rx.text("Định nghĩa", color=T.TEXT_SECONDARY, font_weight="600"),
                rx.box(
                    rx.text(
                        FolderState.current_question_display,
                        font_size="1.35rem",
                        font_weight="700",
                        color=T.TEXT_PRIMARY,
                    ),
                    padding="1.1rem",
                    bg=T.SURFACE,
                    border_radius=T.RADIUS_MD,
                    border=f"1px solid {T.BORDER}",
                    width="100%",
                    box_shadow=T.SHADOW_CARD,
                ),
                flex="1",
            ),
            rx.box(width="1px", bg=T.BORDER),
            rx.vstack(
                rx.text("Thuật ngữ", color=T.TEXT_SECONDARY, font_weight="600", align_self="flex-end"),
                rx.box(
                    rx.text(
                        FolderState.dung_sai_candidate,
                        font_size="1.25rem",
                        font_weight="700",
                        text_align="right",
                        color=T.TEXT_PRIMARY,
                    ),
                    padding="1.1rem",
                    bg=T.SURFACE,
                    border_radius=T.RADIUS_MD,
                    border=f"1px solid {T.BORDER}",
                    width="100%",
                    align_self="flex-end",
                    box_shadow=T.SHADOW_CARD,
                ),
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
            rx.text(
                "Bạn không biết?",
                color=T.PRIMARY,
                font_weight="700",
                cursor="pointer",
                on_click=lambda: FolderState.set_selected_answer(FolderState.correct_answer),
                _hover={"text_decoration": "underline"},
            ),
            rx.spacer(),
            rx.button(
                "Tiếp",
                on_click=FolderState.next_test_question,
                bg=rx.cond(FolderState.selected_answer != "", T.PRIMARY, T.PRIMARY_DISABLED),
                color="white",
                font_weight="700",
                border_radius=T.RADIUS_PILL,
                padding="0.65rem 1.4rem",
                cursor=rx.cond(FolderState.selected_answer != "", "pointer", "not-allowed"),
                _hover={"bg": T.PRIMARY_HOVER},
            ),
        ),
        spacing="4",
        width="100%",
    )
