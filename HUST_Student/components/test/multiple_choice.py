import reflex as rx

from HUST_Student.components.ui import theme as T
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
                    rx.cond(
                        is_correct,
                        T.SUCCESS,
                        rx.cond(is_selected, T.DANGER, T.TEXT_MUTED),
                    ),
                    T.TEXT_PRIMARY,
                ),
                flex="1",
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
        width="100%",
        padding="1.1rem 1.25rem",
        border=rx.cond(
            has_answered & is_correct,
            f"2px solid {T.SUCCESS}",
            rx.cond(
                has_answered & is_selected & ~is_correct,
                f"2px solid {T.DANGER}",
                f"1.5px solid {T.BORDER}",
            ),
        ),
        border_radius=T.RADIUS_MD,
        bg=rx.cond(
            has_answered,
            rx.cond(is_correct, T.SUCCESS_BG, rx.cond(is_selected, T.DANGER_BG, T.SURFACE)),
            T.SURFACE,
        ),
        cursor=rx.cond(has_answered, "default", "pointer"),
        on_click=lambda: FolderState.set_selected_answer(option),
        _hover=rx.cond(
            has_answered,
            {},
            {
                "bg": T.PRIMARY_TINT,
                "border_color": T.PRIMARY,
            },
        ),
        transition="all 0.15s ease",
    )


def trac_nghiem_section():
    question_label = rx.cond(FolderState.answer_language == "Foreign", "Native", "Foreign")

    return rx.vstack(
        rx.hstack(
            rx.text(
                question_label,
                font_size="0.8rem",
                font_weight="700",
                color=T.TEXT_MUTED,
                text_transform="uppercase",
                letter_spacing="0.08em",
            ),
            rx.spacer(),
            rx.text(
                FolderState.current_test_index + 1,
                " / ",
                FolderState.test_question_count,
                font_weight="700",
                color=T.TEXT_SECONDARY,
                font_size="0.9rem",
            ),
            width="100%",
            align="center",
        ),
        rx.progress(
            value=rx.cond(
                FolderState.test_question_count > 0,
                ((FolderState.current_test_index + 1) * 100) // FolderState.test_question_count,
                0,
            ),
            max=100,
            width="100%",
            color_scheme="blue",
            size="2",
        ),
        rx.box(
            rx.text(
                FolderState.current_question_display,
                font_size="1.5rem",
                font_weight="700",
                color=T.TEXT_PRIMARY,
                text_align="center",
                line_height="1.35",
            ),
            padding="1.75rem",
            border=f"1px solid {T.BORDER}",
            border_radius=T.RADIUS_LG,
            bg=T.SURFACE,
            width="100%",
            min_height="120px",
            display="flex",
            align_items="center",
            justify_content="center",
            box_shadow=T.SHADOW_CARD,
        ),
        rx.text(
            "Chọn đáp án đúng",
            font_size="0.85rem",
            color=T.TEXT_SECONDARY,
            font_weight="600",
        ),
        rx.grid(
            rx.foreach(FolderState.current_options, answer_option_button),
            template_columns="repeat(2, minmax(0, 1fr))",
            gap="3",
            width="100%",
        ),
        rx.vstack(
            rx.text(
                "Bạn không biết?",
                color=T.PRIMARY,
                font_weight="700",
                font_size="0.9rem",
                cursor="pointer",
                align_self="center",
                on_click=FolderState.show_hint,
                _hover={"text_decoration": "underline"},
            ),
            rx.cond(
                FolderState.hint_text != "",
                rx.text(
                    FolderState.hint_text,
                    font_size="0.85rem",
                    color=T.TEXT_SECONDARY,
                    text_align="center",
                ),
            ),
            spacing="1",
            align="center",
        ),
        rx.hstack(
            rx.button(
                "Đóng",
                on_click=FolderState.close_test,
                bg=T.BORDER_LIGHT,
                color=T.TEXT_PRIMARY,
                border_radius=T.RADIUS_MD,
                padding="0.65rem 1.2rem",
                font_weight="600",
                _hover={"bg": T.BORDER},
            ),
            rx.spacer(),
            rx.button(
                "Tiếp theo →",
                on_click=FolderState.next_test_question,
                bg=rx.cond(
                    FolderState.selected_answer != "",
                    T.PRIMARY,
                    T.PRIMARY_DISABLED,
                ),
                color="white",
                font_weight="700",
                border_radius=T.RADIUS_MD,
                padding="0.65rem 1.35rem",
                _hover={"bg": T.PRIMARY_HOVER, "cursor": "pointer"},
                cursor=rx.cond(FolderState.selected_answer != "", "pointer", "not-allowed"),
            ),
            width="100%",
            align="center",
        ),
        spacing="4",
        width="100%",
    )
