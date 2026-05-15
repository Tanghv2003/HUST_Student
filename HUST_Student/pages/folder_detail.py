import reflex as rx

from HUST_Student.states.folder_state import FolderState
from HUST_Student.states.navigation_state import NavigationState
from HUST_Student.components.true_false_mode import true_false_section


# ══════════════════════════════════════════════════════════════════
# SHARED HELPERS
# ══════════════════════════════════════════════════════════════════

def _modal_close_btn(on_click):
    return rx.button(
        rx.icon("x", size=18),
        on_click=on_click,
        bg="transparent",
        color="#6B7280",
        border_radius="8px",
        padding="0.4rem",
        _hover={"bg": "#F3F4F6"},
    )


def option_button(icon: str, label: str, on_click=None):
    return rx.vstack(
        rx.icon(icon, size=32, color="#4F46E5"),
        rx.text(label, font_size="0.9rem", font_weight="600", text_align="center"),
        align="center",
        spacing="2",
        padding="1.5rem",
        border="1px solid #E5E7EB",
        border_radius="12px",
        bg="white",
        cursor="pointer",
        on_click=on_click,
        _hover={"bg": "#EEF2FF", "border_color": "#4F46E5"},
    )


# ══════════════════════════════════════════════════════════════════
# LEARN MODE OVERLAY
# ══════════════════════════════════════════════════════════════════

def _learn_progress_bar():
    #total = rx.cond(len(FolderState.learn_cards) > 0, len(FolderState.learn_cards), 1)
    total = rx.cond(FolderState.learn_cards.length() > 0, FolderState.learn_cards.length(), 1)
    mastered_pct = FolderState.learn_mastered_pct

    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.box(width="9px", height="9px", border_radius="999px", bg="#16A34A"),
                rx.text(FolderState.learn_mastered_count, " thành thạo",
                        font_size="0.75rem", color="#16A34A", font_weight="600"),
                spacing="1", align="center",
            ),
            rx.hstack(
                rx.box(width="9px", height="9px", border_radius="999px", bg="#F59E0B"),
                rx.text(FolderState.learn_learning_count, " đang học",
                        font_size="0.75rem", color="#F59E0B", font_weight="600"),
                spacing="1", align="center",
            ),
            rx.hstack(
                rx.box(width="9px", height="9px", border_radius="999px", bg="#D1D5DB"),
                rx.text(FolderState.learn_not_started_count, " chưa học",
                        font_size="0.75rem", color="#9CA3AF", font_weight="600"),
                spacing="1", align="center",
            ),
            spacing="4",
        ),
        rx.box(
            rx.box(
                height="100%",
                width=f"{mastered_pct}%",
                bg="linear-gradient(90deg, #16A34A, #22C55E)",
                border_radius="999px",
                transition="width 0.5s ease",
            ),
            width="100%", height="7px", bg="#E5E7EB", border_radius="999px", overflow="hidden",
        ),
        spacing="2", width="100%",
    )


def _learn_phase_badge():
    label = rx.cond(
        FolderState.learn_phase == "preview", "Xem thẻ",
        rx.cond(
            FolderState.learn_phase == "type", "Gõ đáp án",
            rx.cond(
                FolderState.learn_phase == "choice", "Trắc nghiệm",
                "Ôn lại",
            ),
        ),
    )
    bg = rx.cond(
        FolderState.learn_phase == "preview", "#E0F2FE",
        rx.cond(FolderState.learn_phase == "type", "#EDE9FE",
                rx.cond(FolderState.learn_phase == "choice", "#FEF3C7", "#FCE7F3")),
    )
    color = rx.cond(
        FolderState.learn_phase == "preview", "#0369A1",
        rx.cond(FolderState.learn_phase == "type", "#6D28D9",
                rx.cond(FolderState.learn_phase == "choice", "#B45309", "#BE185D")),
    )
    return rx.box(
        rx.text(label, font_size="0.72rem", font_weight="700", color=color),
        bg=bg, border_radius="999px", padding="0.2rem 0.7rem",
    )


# ── Preview phase ──────────────────────────────────────────────────

def _learn_preview():
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.text(
                    rx.cond(FolderState.learn_is_preview_flipped, "Nghĩa", "Thuật ngữ"),
                    font_size="0.75rem", font_weight="700", color="#A78BFA",
                    text_transform="uppercase", letter_spacing="0.08em",
                ),
                rx.text(
                    rx.cond(
                        FolderState.learn_is_preview_flipped,
                        FolderState.learn_card_back,
                        FolderState.learn_card_front,
                    ),
                    font_size="1.9rem", font_weight="700", color="#1E1B4B",
                    text_align="center", line_height="1.3",
                ),
                rx.text("Nhấp để lật thẻ", font_size="0.75rem", color="#C4B5FD", margin_top="0.5rem"),
                spacing="3", align="center", justify="center", height="100%",
            ),
            width="100%", min_height="190px",
            bg="linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%)",
            border="2px solid #DDD6FE", border_radius="20px",
            padding="2rem", cursor="pointer",
            on_click=FolderState.learn_flip_preview,
            display="flex", align_items="center", justify_content="center",
            transition="all 0.18s ease",
            _hover={"border_color": "#8B5CF6", "box_shadow": "0 6px 20px rgba(139,92,246,0.15)"},
        ),
        rx.hstack(
            rx.button(
                rx.hstack(rx.icon("rotate-ccw", size=15), rx.text("Vẫn đang học"), spacing="2", align="center"),
                on_click=FolderState.learn_preview_still_learning,
                bg="white", color="#374151",
                border="2px solid #E5E7EB", border_radius="12px",
                padding="0.7rem 1.2rem", font_weight="600",
                _hover={"bg": "#F9FAFB", "border_color": "#D1D5DB"},
                flex="1",
            ),
            rx.button(
                rx.hstack(rx.icon("check", size=15), rx.text("Đã biết"), spacing="2", align="center"),
                on_click=FolderState.learn_preview_got_it,
                bg="#4F46E5", color="white",
                border_radius="12px", padding="0.7rem 1.2rem", font_weight="600",
                _hover={"bg": "#4338CA"},
                flex="1",
            ),
            spacing="3", width="100%",
        ),
        spacing="4", width="100%",
    )


# ── Type phase ─────────────────────────────────────────────────────

def _learn_type():
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.text("Nghĩa", font_size="0.72rem", font_weight="700", color="#9CA3AF",
                        text_transform="uppercase", letter_spacing="0.08em"),
                rx.text(FolderState.learn_card_front, font_size="1.5rem", font_weight="700",
                        color="#111827", text_align="center", line_height="1.3"),
                spacing="2", align="center",
            ),
            width="100%", padding="1.4rem 1.8rem",
            bg="#F8FAFC", border="1.5px solid #E5E7EB", border_radius="16px", text_align="center",
        ),

        rx.cond(
            FolderState.learn_show_feedback,
            # Feedback box
            rx.vstack(
                rx.box(
                    rx.text(
                        FolderState.learn_feedback_message,
                        font_size="0.95rem", font_weight="600",
                        color=rx.cond(FolderState.learn_feedback_correct, "#15803D", "#B91C1C"),
                        text_align="center",
                    ),
                    width="100%", padding="1rem 1.2rem",
                    bg=rx.cond(FolderState.learn_feedback_correct, "#F0FDF4", "#FFF5F5"),
                    border=rx.cond(FolderState.learn_feedback_correct,
                                   "1.5px solid #BBF7D0", "1.5px solid #FECACA"),
                    border_radius="14px",
                ),
                rx.button(
                    "Tiếp theo →",
                    on_click=FolderState.learn_continue_after_type,
                    bg=rx.cond(FolderState.learn_feedback_correct, "#16A34A", "#DC2626"),
                    color="white", border_radius="12px",
                    padding="0.65rem 1.5rem", font_weight="700", width="100%",
                    _hover={"opacity": "0.9"},
                ),
                spacing="3", width="100%",
            ),
            # Input box
            rx.vstack(
                rx.text("Gõ thuật ngữ", font_size="0.82rem", color="#6B7280", font_weight="500"),
                rx.hstack(
                    rx.input(
                        value=FolderState.learn_typed_answer,
                        on_change=FolderState.learn_set_typed,
                        placeholder="Nhập đáp án...",
                        width="100%", height="50px",
                        bg="white", border="2px solid #E5E7EB", border_radius="12px",
                        font_size="1.05rem", padding="0 1rem",
                        _focus={"border_color": "#4F46E5", "box_shadow": "0 0 0 3px rgba(79,70,229,0.1)"},
                    ),
                    rx.button(
                        rx.icon("send", size=17),
                        on_click=FolderState.learn_submit_typed,
                        bg=rx.cond(FolderState.learn_typed_answer != "", "#4F46E5", "#C7D2FE"),
                        color="white", border_radius="12px", height="50px", width="50px",
                        cursor=rx.cond(FolderState.learn_typed_answer != "", "pointer", "not-allowed"),
                    ),
                    width="100%", spacing="2",
                ),
                spacing="2", width="100%",
            ),
        ),
        spacing="4", width="100%",
    )


# ── Choice phase ───────────────────────────────────────────────────

def _learn_choice_btn(option: str):
    is_selected = FolderState.learn_selected_choice == option
    is_correct = FolderState.learn_correct_answer == option
    has_answered = FolderState.learn_selected_choice != ""

    return rx.box(
        rx.hstack(
            rx.text(
                option,
                font_size="0.97rem", font_weight="600",
                color=rx.cond(
                    has_answered,
                    rx.cond(is_correct, "#15803D", rx.cond(is_selected, "#B91C1C", "#9CA3AF")),
                    "#111827",
                ),
                flex="1",
            ),
            rx.cond(
                has_answered & is_correct,
                rx.icon("check", size=16, color="#16A34A"),
                rx.cond(
                    has_answered & is_selected & ~is_correct,
                    rx.icon("x", size=16, color="#DC2626"),
                    rx.box(),
                ),
            ),
            align="center", width="100%",
        ),
        width="100%", padding="0.85rem 1.1rem",
        border=rx.cond(
            has_answered,
            rx.cond(is_correct, "2px solid #16A34A",
                    rx.cond(is_selected, "2px solid #DC2626", "1.5px solid #E5E7EB")),
            rx.cond(is_selected, "2px solid #4F46E5", "1.5px solid #E5E7EB"),
        ),
        border_radius="13px",
        bg=rx.cond(
            has_answered,
            rx.cond(is_correct, "#DCFCE7", rx.cond(is_selected, "#FEE2E2", "white")),
            "white",
        ),
        cursor=rx.cond(has_answered, "default", "pointer"),
        on_click=lambda: FolderState.learn_select_choice(option),
        _hover=rx.cond(has_answered, {}, {"bg": "#F5F3FF", "border_color": "#4F46E5"}),
        transition="all 0.14s ease",
    )


def _learn_choice():
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.text("Nghĩa", font_size="0.72rem", font_weight="700", color="#9CA3AF",
                        text_transform="uppercase", letter_spacing="0.08em"),
                rx.text(FolderState.learn_card_front, font_size="1.4rem", font_weight="700",
                        color="#111827", text_align="center", line_height="1.3"),
                spacing="2", align="center",
            ),
            width="100%", padding="1.3rem 1.6rem",
            bg="#FFFBEB", border="1.5px solid #FDE68A", border_radius="16px", text_align="center",
        ),
        rx.text("Chọn thuật ngữ đúng", font_size="0.8rem", color="#6B7280", font_weight="500"),
        rx.grid(
            rx.foreach(FolderState.learn_choice_options, _learn_choice_btn),
            template_columns="repeat(2, minmax(0, 1fr))",
            gap="3", width="100%",
        ),
        rx.cond(
            FolderState.learn_show_feedback,
            rx.button(
                "Tiếp theo →",
                on_click=FolderState.learn_continue_after_choice,
                bg=rx.cond(FolderState.learn_feedback_correct, "#16A34A", "#DC2626"),
                color="white", border_radius="12px",
                padding="0.65rem 2rem", font_weight="700", width="100%",
                _hover={"opacity": "0.9"},
            ),
            rx.box(),
        ),
        spacing="4", width="100%",
    )


# ── Review summary ─────────────────────────────────────────────────

def _learn_review_summary():
    return rx.vstack(
        rx.vstack(
            rx.icon("refresh-cw", size=38, color="#F59E0B"),
            rx.text(
                "Ôn lại — Vòng ", FolderState.learn_round,
                font_size="1.4rem", font_weight="700", color="#111827",
            ),
            rx.text(
                "Bạn còn một số thẻ cần luyện thêm. Hãy tiếp tục!",
                font_size="0.9rem", color="#6B7280", text_align="center",
            ),
            spacing="2", align="center",
        ),
        rx.hstack(
            rx.vstack(
                rx.text(FolderState.learn_total_correct, font_size="2rem", font_weight="800", color="#16A34A"),
                rx.text("Đúng", font_size="0.8rem", color="#6B7280"),
                align="center",
            ),
            rx.box(width="1px", height="48px", bg="#E5E7EB"),
            rx.vstack(
                rx.text(FolderState.learn_total_wrong, font_size="2rem", font_weight="800", color="#DC2626"),
                rx.text("Sai", font_size="0.8rem", color="#6B7280"),
                align="center",
            ),
            rx.box(width="1px", height="48px", bg="#E5E7EB"),
            rx.vstack(
                rx.text(FolderState.learn_mastered_count, font_size="2rem", font_weight="800", color="#4F46E5"),
                rx.text("Thành thạo", font_size="0.8rem", color="#6B7280"),
                align="center",
            ),
            spacing="6", justify="center", width="100%",
        ),
        rx.button(
            "Tiếp tục luyện tập →",
            on_click=FolderState.learn_continue_review_round,
            bg="#F59E0B", color="white", border_radius="14px",
            padding="0.9rem 2rem", font_weight="700", font_size="0.95rem",
            width="100%", _hover={"bg": "#D97706"},
        ),
        spacing="5", align="center", padding_y="0.5rem", width="100%",
    )


# ── Complete ───────────────────────────────────────────────────────

def _learn_complete():
    return rx.vstack(
        rx.vstack(
            rx.text("🎉", font_size="3rem"),
            rx.text("Xuất sắc!", font_size="1.7rem", font_weight="800", color="#111827"),
            rx.text(
                "Bạn đã thành thạo toàn bộ học phần này!",
                font_size="0.92rem", color="#6B7280", text_align="center",
            ),
            spacing="2", align="center",
        ),
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        FolderState.learn_accuracy_pct, "%",
                        font_size="2rem", font_weight="800",
                        color=rx.cond(FolderState.learn_accuracy_pct >= 70, "#16A34A", "#F59E0B"),
                    ),
                    rx.text("Chính xác", font_size="0.78rem", color="#6B7280"),
                    align="center",
                ),
                rx.box(width="1px", height="55px", bg="#E5E7EB"),
                rx.vstack(
                    rx.text(FolderState.learn_mastered_count, font_size="2rem", font_weight="800", color="#4F46E5"),
                    rx.text("Thành thạo", font_size="0.78rem", color="#6B7280"),
                    align="center",
                ),
                rx.box(width="1px", height="55px", bg="#E5E7EB"),
                rx.vstack(
                    rx.text(FolderState.learn_round, font_size="2rem", font_weight="800", color="#F59E0B"),
                    rx.text("Vòng học", font_size="0.78rem", color="#6B7280"),
                    align="center",
                ),
                spacing="6", justify="center", width="100%",
            ),
            bg="#F8FAFC", border="1.5px solid #E5E7EB",
            border_radius="16px", padding="1.4rem", width="100%",
        ),
        rx.button(
            rx.hstack(rx.icon("x", size=15), rx.text("Đóng"), spacing="2"),
            on_click=FolderState.close_learn,
            bg="#4F46E5", color="white", border_radius="12px",
            padding="0.75rem 2rem", font_weight="700", width="100%",
            _hover={"bg": "#4338CA"},
        ),
        spacing="5", align="center", width="100%",
    )


# ── Phase router ───────────────────────────────────────────────────

def _learn_phase_router():
    return rx.cond(
        FolderState.learn_phase == "preview", _learn_preview(),
        rx.cond(
            FolderState.learn_phase == "type", _learn_type(),
            rx.cond(
                FolderState.learn_phase == "choice", _learn_choice(),
                rx.cond(
                    FolderState.learn_phase == "review", _learn_review_summary(),
                    _learn_complete(),
                ),
            ),
        ),
    )


def learn_overlay():
    return rx.cond(
        FolderState.show_learn,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                rx.cond(FolderState.selected_set, FolderState.selected_set.title, ""),
                                font_size="1.1rem", font_weight="700", color="#111827",
                            ),
                            rx.hstack(
                                _learn_phase_badge(),
                                rx.text(
                                    FolderState.learn_queue_label,
                                    font_size="0.78rem", color="#6B7280", font_weight="600",
                                ),
                                spacing="2", align="center",
                            ),
                            spacing="1", align="start",
                        ),
                        rx.spacer(),
                        _modal_close_btn(FolderState.close_learn),
                        width="100%", align="center",
                    ),

                    # Progress (ẩn khi complete)
                    rx.cond(
                        FolderState.learn_phase != "complete",
                        _learn_progress_bar(),
                        rx.box(),
                    ),

                    rx.divider(),

                    # Phase content
                    _learn_phase_router(),

                    spacing="5",
                    padding="1.8rem 2rem 2rem",
                    width="100%",
                ),
                bg="white",
                border_radius="24px",
                width="560px",
                max_width="95vw",
                max_height="92vh",
                overflow_y="auto",
                box_shadow="0 20px 60px rgba(0,0,0,0.16)",
                on_click=rx.stop_propagation,
            ),
            position="fixed",
            top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg="rgba(17,24,39,0.45)",
            z_index="1000",
            padding="1.5rem",
            on_click=FolderState.close_learn,
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# TEST MODALS
# ══════════════════════════════════════════════════════════════════

def test_option_button(label: str, mode: str):
    return rx.button(
        label,
        on_click=lambda: FolderState.set_test_mode(mode),
        width="100%",
        padding="1rem",
        border_radius="999px",
        border="1px solid #E5E7EB",
        bg=rx.cond(FolderState.test_mode == mode, "#4F46E5", "#F8FAFC"),
        color=rx.cond(FolderState.test_mode == mode, "white", "#111827"),
        _hover={"bg": "#E5F2FF"},
    )


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


def test_run_modal():
    mode_label = rx.cond(
        FolderState.test_mode == "dung_sai", "Đúng/Sai",
        rx.cond(FolderState.test_mode == "trac_nghiem", "Trắc nghiệm",
                rx.cond(FolderState.test_mode == "ghep_the", "Ghép thẻ", "Tự luận")),
    )

    return rx.cond(
        FolderState.show_test,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                rx.cond(FolderState.selected_set, FolderState.selected_set.title, "Kiểm tra"),
                                font_size="1.3rem", font_weight="700",
                            ),
                            rx.hstack(
                                rx.badge(mode_label, color_scheme="indigo", variant="soft", size="1"),
                                rx.badge(FolderState.answer_language, color_scheme="gray", variant="soft", size="1"),
                                spacing="2",
                            ),
                            spacing="1", align="start",
                        ),
                        rx.spacer(),
                        _modal_close_btn(FolderState.close_test),
                        width="100%", align="center",
                    ),
                    rx.divider(),
                    rx.cond(
                        FolderState.test_mode == "trac_nghiem",
                        trac_nghiem_section(),
                        rx.cond(
                            FolderState.test_mode == "dung_sai",
                            true_false_section(),
                            rx.cond(
                                FolderState.test_mode == "tu_luan",
                                # Essay mode
                                rx.vstack(
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
                                ),
                                rx.vstack(
                                    rx.text("Chế độ này đang được phát triển.", color="#6B7280", text_align="center"),
                                    rx.button("Đóng", on_click=FolderState.close_test, bg="#F3F4F6"),
                                    spacing="4", align="center", padding_y="2rem",
                                ),
                            ),
                        ),
                    ),
                    spacing="5", padding="1.8rem 2rem 2rem", width="100%",
                ),
                bg="white", border_radius="24px", width="580px", max_width="95vw",
                box_shadow="0 20px 60px rgba(0,0,0,0.14)",
                on_click=rx.stop_propagation,
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg="rgba(17,24,39,0.4)", z_index="999", padding="1.5rem",
            on_click=FolderState.close_test,
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# SET OPTIONS MODAL
# ══════════════════════════════════════════════════════════════════

def set_options_modal():
    return rx.cond(
        FolderState.show_set_options,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(FolderState.selected_set.title, font_size="1.5rem", font_weight="700"),
                        rx.spacer(),
                        _modal_close_btn(FolderState.close_set_options),
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


# ══════════════════════════════════════════════════════════════════
# TEST OPTIONS MODAL
# ══════════════════════════════════════════════════════════════════

def test_options_modal():
    return rx.cond(
        FolderState.show_test_options,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(FolderState.selected_set.title, font_size="1.5rem", font_weight="700"),
                            rx.text("Thiết lập bài kiểm tra", color="#6B7280", font_size="0.95rem"),
                            spacing="1", align="start",
                        ),
                        rx.spacer(),
                        _modal_close_btn(FolderState.close_test_options),
                        width="100%", align="center",
                    ),
                    rx.divider(),
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.text("Số câu hỏi", font_weight="600"),
                                rx.text(
                                    rx.cond(FolderState.selected_set, FolderState.selected_set.terms, 0),
                                    " câu", color="#111827",
                                ),
                            ),
                            rx.vstack(
                                rx.text("Tối đa", font_weight="600"),
                                rx.text(
                                    rx.cond(FolderState.selected_set, FolderState.selected_set.terms, 0),
                                    " câu", color="#6B7280",
                                ),
                            ),
                            rx.vstack(
                                rx.text("Trả lời bằng", font_weight="600"),
                                rx.select(
                                    ["Cả hai", "Native", "Foreign"],
                                    value=FolderState.answer_language,
                                    on_change=FolderState.set_answer_language,
                                    width="160px",
                                    border="1px solid #E5E7EB",
                                    border_radius="14px",
                                    padding="0.9rem 1rem",
                                ),
                            ),
                            spacing="8", width="100%",
                        ),
                        rx.text("Loại câu hỏi", font_weight="600"),
                        rx.grid(
                            test_option_button("Đúng/Sai", "dung_sai"),
                            test_option_button("Trắc nghiệm", "trac_nghiem"),
                            test_option_button("Ghép thẻ", "ghep_the"),
                            test_option_button("Tự luận", "tu_luan"),
                            template_columns="repeat(2, minmax(0, 1fr))",
                            gap="4", width="100%",
                        ),
                        rx.button(
                            "Bắt đầu làm kiểm tra",
                            on_click=FolderState.start_test,
                            bg="#4F46E5", color="white", border_radius="999px",
                            padding="1rem 1.5rem", _hover={"bg": "#4338CA"}, width="100%",
                        ),
                        spacing="4", width="100%",
                    ),
                    spacing="6", padding="2rem", width="100%",
                ),
                bg="white", border_radius="24px", width="560px", max_width="95%",
                box_shadow="0 20px 60px rgba(0,0,0,0.12)",
                on_click=rx.stop_propagation,
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg="rgba(0,0,0,0.35)", z_index="999", padding="1.5rem",
            on_click=FolderState.close_test_options,
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# RESULT OVERLAY
# ══════════════════════════════════════════════════════════════════

def answer_record_row(record):
    return rx.box(
        rx.hstack(
            rx.cond(
                record.is_correct,
                rx.box(
                    rx.icon("check", size=16, color="#16A34A"),
                    bg="#DCFCE7", border_radius="999px", padding="0.3rem",
                    display="flex", align_items="center", justify_content="center", flex_shrink="0",
                ),
                rx.box(
                    rx.icon("x", size=16, color="#DC2626"),
                    bg="#FEE2E2", border_radius="999px", padding="0.3rem",
                    display="flex", align_items="center", justify_content="center", flex_shrink="0",
                ),
            ),
            rx.vstack(
                rx.text(record.question, font_size="0.85rem", color="#6B7280"),
                rx.text(record.correct, font_size="1rem", font_weight="600", color="#111827"),
                rx.cond(
                    ~record.is_correct,
                    rx.hstack(
                        rx.text("Bạn chọn: ", font_size="0.82rem", color="#9CA3AF"),
                        rx.text(record.chosen, font_size="0.82rem", color="#DC2626", font_weight="600"),
                        spacing="1", align="center",
                    ),
                    rx.box(),
                ),
                spacing="1", align="start", flex="1",
            ),
            spacing="3", align="start", width="100%",
        ),
        padding="1rem 1.2rem",
        border_radius="14px",
        border=rx.cond(record.is_correct, "1px solid #BBF7D0", "1px solid #FECACA"),
        bg=rx.cond(record.is_correct, "#F0FDF4", "#FFF5F5"),
        width="100%",
    )


def result_overlay():
    total = FolderState.score_correct + FolderState.score_wrong
    pct = rx.cond(total > 0, (FolderState.score_correct * 100) // total, 0)

    return rx.cond(
        FolderState.show_result,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                rx.cond(FolderState.selected_set, FolderState.selected_set.title, "Kết quả"),
                                font_size="1.3rem", font_weight="700",
                            ),
                            rx.text("Hoàn thành bài kiểm tra", color="#6B7280", font_size="0.9rem"),
                            spacing="1",
                        ),
                        rx.spacer(),
                        _modal_close_btn(FolderState.close_test),
                        width="100%", align="center",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.vstack(
                            rx.box(
                                rx.vstack(
                                    rx.text(pct, "%", font_size="1.8rem", font_weight="700",
                                            color=rx.cond(pct >= 70, "#16A34A", "#DC2626")),
                                    spacing="0", align="center",
                                ),
                                width="100px", height="100px", border_radius="999px",
                                border=rx.cond(pct >= 70, "6px solid #16A34A", "6px solid #DC2626"),
                                display="flex", align_items="center", justify_content="center",
                            ),
                            rx.text(rx.cond(pct >= 70, "Tốt lắm! 🎉", "Cố lên! 💪"),
                                    font_size="0.85rem", color="#6B7280", text_align="center"),
                            spacing="2", align="center",
                        ),
                        rx.vstack(
                            rx.hstack(
                                rx.box(width="12px", height="12px", border_radius="999px", bg="#16A34A"),
                                rx.text("Đúng", font_weight="600", flex="1"),
                                rx.box(
                                    rx.text(FolderState.score_correct, color="#16A34A", font_weight="700", font_size="1.1rem"),
                                    bg="#DCFCE7", border_radius="8px", padding="0.2rem 0.8rem",
                                ),
                                spacing="3", align="center", width="200px",
                            ),
                            rx.hstack(
                                rx.box(width="12px", height="12px", border_radius="999px", bg="#DC2626"),
                                rx.text("Sai", font_weight="600", flex="1"),
                                rx.box(
                                    rx.text(FolderState.score_wrong, color="#DC2626", font_weight="700", font_size="1.1rem"),
                                    bg="#FEE2E2", border_radius="8px", padding="0.2rem 0.8rem",
                                ),
                                spacing="3", align="center", width="200px",
                            ),
                            spacing="3", align="start", flex="1",
                        ),
                        rx.vstack(
                            rx.button(
                                rx.icon("refresh-cw", size=14), " Làm lại tất cả",
                                on_click=FolderState.retry_all,
                                bg="#4F46E5", color="white", border_radius="10px",
                                width="100%", _hover={"bg": "#4338CA"},
                            ),
                            rx.button(
                                rx.icon("x-circle", size=14), " Luyện câu sai",
                                on_click=FolderState.retry_wrong_only,
                                bg="white", color="#DC2626",
                                border="1px solid #FECACA", border_radius="10px",
                                width="100%", _hover={"bg": "#FFF5F5"},
                            ),
                            spacing="2", width="140px",
                        ),
                        spacing="6", width="100%", align="center",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.text("Đáp án của bạn", font_weight="700", font_size="1rem"),
                        rx.spacer(),
                        rx.hstack(
                            rx.button(
                                "Tất cả",
                                on_click=FolderState.set_show_wrong_only(False),
                                bg=rx.cond(~FolderState.show_wrong_only, "#4F46E5", "#F3F4F6"),
                                color=rx.cond(~FolderState.show_wrong_only, "white", "#374151"),
                                border_radius="8px", size="2", padding="0.3rem 0.8rem",
                            ),
                            rx.button(
                                "Câu sai",
                                on_click=FolderState.set_show_wrong_only(True),
                                bg=rx.cond(FolderState.show_wrong_only, "#DC2626", "#F3F4F6"),
                                color=rx.cond(FolderState.show_wrong_only, "white", "#374151"),
                                border_radius="8px", size="2", padding="0.3rem 0.8rem",
                            ),
                            spacing="2",
                        ),
                        width="100%", align="center",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                FolderState.answer_records,
                                lambda record: rx.cond(
                                    FolderState.show_wrong_only & record.is_correct,
                                    rx.box(),
                                    answer_record_row(record),
                                ),
                            ),
                            spacing="2", width="100%",
                        ),
                        max_height="320px", overflow_y="auto", width="100%", padding_right="4px",
                    ),
                    spacing="5", padding="1.8rem 2rem 2rem", width="100%",
                ),
                bg="white", border_radius="24px", width="620px", max_width="95vw",
                max_height="90vh", overflow_y="auto",
                box_shadow="0 20px 60px rgba(0,0,0,0.14)",
                on_click=rx.stop_propagation,
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg="rgba(17,24,39,0.4)", z_index="999", padding="1.5rem",
            on_click=FolderState.close_test,
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# FLASHCARD OVERLAY
# ══════════════════════════════════════════════════════════════════

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


# ══════════════════════════════════════════════════════════════════
# STUDYSET CARD + PAGE
# ══════════════════════════════════════════════════════════════════

def studyset_card(title, terms):
    return rx.box(
        rx.vstack(
            rx.text(title, font_size="1.3rem", font_weight="700"),
            rx.text(f"{terms} thuật ngữ", color="#6B7280"),
            align="start", spacing="1",
        ),
        padding="1.2rem",
        border="1px solid #E5E7EB",
        border_radius="16px",
        bg="white",
        width="100%",
        cursor="pointer",
        on_click=lambda: FolderState.select_set(title),
        _hover={"bg": "#F9FAFB", "border_color": "#4F46E5"},
    )


def folder_detail_page():
    return rx.vstack(
        # All overlays / modals
        set_options_modal(),
        test_options_modal(),
        test_run_modal(),
        result_overlay(),
        flashcard_overlay(),
        learn_overlay(),

        # Page content
        rx.text(
            NavigationState.current_folder,
            font_size="2.5rem",
            font_weight="700",
        ),
        rx.vstack(
            rx.foreach(
                FolderState.current_sets,
                lambda item: studyset_card(item.title, item.terms),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        spacing="6",
    )