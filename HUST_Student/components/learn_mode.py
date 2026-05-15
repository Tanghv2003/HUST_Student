import reflex as rx
from HUST_Student.states.learn_state import LearnState


# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════

def _progress_bar():
    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.box(width="10px", height="10px", border_radius="999px", bg="#16A34A"),
                rx.text(LearnState.mastered_count, " thành thạo", font_size="0.78rem", color="#16A34A", font_weight="600"),
                spacing="1", align="center",
            ),
            rx.hstack(
                rx.box(width="10px", height="10px", border_radius="999px", bg="#F59E0B"),
                rx.text(LearnState.learning_count, " đang học", font_size="0.78rem", color="#F59E0B", font_weight="600"),
                spacing="1", align="center",
            ),
            rx.hstack(
                rx.box(width="10px", height="10px", border_radius="999px", bg="#E5E7EB"),
                rx.text(LearnState.not_started_count, " chưa học", font_size="0.78rem", color="#9CA3AF", font_weight="600"),
                spacing="1", align="center",
            ),
            spacing="5",
        ),
        rx.box(
            rx.box(
                height="100%",
                width=f"{LearnState.mastered_count * 100 // rx.cond(len(LearnState.cards) > 0, len(LearnState.cards), 1)}%",
                bg="#16A34A",
                border_radius="999px",
                transition="width 0.4s ease",
            ),
            width="100%",
            height="8px",
            bg="#E5E7EB",
            border_radius="999px",
            overflow="hidden",
        ),
        width="100%",
        spacing="2",
    )


def _phase_badge():
    label = rx.cond(
        LearnState.phase == "preview", "Xem thẻ",
        rx.cond(
            LearnState.phase == "type", "Gõ đáp án",
            rx.cond(
                LearnState.phase == "choice", "Trắc nghiệm",
                "Ôn lại",
            ),
        ),
    )
    color = rx.cond(
        LearnState.phase == "preview", "#E0F2FE",
        rx.cond(
            LearnState.phase == "type", "#EDE9FE",
            rx.cond(
                LearnState.phase == "choice", "#FEF3C7",
                "#FCE7F3",
            ),
        ),
    )
    text_color = rx.cond(
        LearnState.phase == "preview", "#0369A1",
        rx.cond(
            LearnState.phase == "type", "#6D28D9",
            rx.cond(
                LearnState.phase == "choice", "#B45309",
                "#BE185D",
            ),
        ),
    )
    return rx.box(
        rx.text(label, font_size="0.75rem", font_weight="700", color=text_color),
        bg=color,
        border_radius="999px",
        padding="0.25rem 0.75rem",
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE: PREVIEW
# ═══════════════════════════════════════════════════════════════════

def preview_phase():
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.text(
                    rx.cond(LearnState.is_preview_flipped, "Nghĩa", "Thuật ngữ"),
                    font_size="0.8rem",
                    font_weight="600",
                    color="#9CA3AF",
                    text_transform="uppercase",
                    letter_spacing="0.08em",
                ),
                rx.text(
                    rx.cond(
                        LearnState.is_preview_flipped,
                        LearnState.current_card_back,
                        LearnState.current_card_front,
                    ),
                    font_size="2rem",
                    font_weight="700",
                    color="#111827",
                    text_align="center",
                    line_height="1.3",
                ),
                rx.text(
                    "Nhấp để lật thẻ",
                    font_size="0.78rem",
                    color="#C4B5FD",
                    margin_top="1rem",
                ),
                spacing="3",
                align="center",
                justify="center",
                height="100%",
            ),
            width="100%",
            min_height="200px",
            bg="linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%)",
            border="2px solid #DDD6FE",
            border_radius="20px",
            padding="2rem",
            cursor="pointer",
            on_click=LearnState.flip_preview,
            display="flex",
            align_items="center",
            justify_content="center",
            transition="all 0.2s ease",
            _hover={"border_color": "#8B5CF6", "box_shadow": "0 8px 24px rgba(139,92,246,0.15)"},
        ),
        rx.hstack(
            rx.button(
                rx.hstack(
                    rx.icon("rotate-ccw", size=16),
                    rx.text("Vẫn đang học"),
                    spacing="2", align="center",
                ),
                on_click=LearnState.preview_still_learning,
                bg="white",
                color="#374151",
                border="2px solid #E5E7EB",
                border_radius="12px",
                padding="0.75rem 1.5rem",
                font_weight="600",
                _hover={"bg": "#F9FAFB", "border_color": "#D1D5DB"},
                flex="1",
            ),
            rx.button(
                rx.hstack(
                    rx.icon("check", size=16),
                    rx.text("Đã biết"),
                    spacing="2", align="center",
                ),
                on_click=LearnState.preview_got_it,
                bg="#4F46E5",
                color="white",
                border_radius="12px",
                padding="0.75rem 1.5rem",
                font_weight="600",
                _hover={"bg": "#4338CA"},
                flex="1",
            ),
            spacing="3",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE: TYPE
# ═══════════════════════════════════════════════════════════════════

def type_phase():
    return rx.vstack(
        # Question
        rx.box(
            rx.vstack(
                rx.text("Nghĩa", font_size="0.78rem", font_weight="700", color="#9CA3AF",
                        text_transform="uppercase", letter_spacing="0.08em"),
                rx.text(LearnState.current_card_front, font_size="1.6rem", font_weight="700",
                        color="#111827", text_align="center", line_height="1.3"),
                spacing="2", align="center",
            ),
            width="100%",
            padding="1.5rem 2rem",
            bg="#F8FAFC",
            border="1.5px solid #E5E7EB",
            border_radius="16px",
            text_align="center",
        ),

        # Feedback box (hiện sau khi submit)
        rx.cond(
            LearnState.show_feedback,
            rx.box(
                rx.vstack(
                    rx.text(
                        LearnState.feedback_message,
                        font_size="1rem",
                        font_weight="600",
                        color=rx.cond(LearnState.feedback_correct, "#15803D", "#B91C1C"),
                        text_align="center",
                    ),
                    rx.button(
                        "Tiếp theo →",
                        on_click=LearnState.continue_after_type,
                        bg=rx.cond(LearnState.feedback_correct, "#16A34A", "#DC2626"),
                        color="white",
                        border_radius="12px",
                        padding="0.6rem 1.5rem",
                        font_weight="700",
                        _hover={"opacity": "0.9"},
                    ),
                    spacing="3",
                    align="center",
                ),
                width="100%",
                padding="1.2rem",
                bg=rx.cond(LearnState.feedback_correct, "#F0FDF4", "#FFF5F5"),
                border=rx.cond(LearnState.feedback_correct, "1.5px solid #BBF7D0", "1.5px solid #FECACA"),
                border_radius="14px",
            ),
            rx.vstack(
                rx.text("Gõ thuật ngữ tiếng Nhật", font_size="0.85rem", color="#6B7280", font_weight="500"),
                rx.hstack(
                    rx.input(
                        value=LearnState.typed_answer,
                        on_change=LearnState.set_typed_answer,
                        placeholder="Nhập đáp án...",
                        width="100%",
                        height="52px",
                        bg="white",
                        border="2px solid #E5E7EB",
                        border_radius="12px",
                        font_size="1.1rem",
                        padding="0 1rem",
                        _focus={"border_color": "#4F46E5", "box_shadow": "0 0 0 3px rgba(79,70,229,0.1)"},
                        on_key_down=rx.cond(
                            LearnState.typed_answer != "",
                            LearnState.submit_typed,
                            rx.noop(),
                        ),
                    ),
                    rx.button(
                        rx.icon("send", size=18),
                        on_click=LearnState.submit_typed,
                        bg=rx.cond(LearnState.typed_answer != "", "#4F46E5", "#C7D2FE"),
                        color="white",
                        border_radius="12px",
                        height="52px",
                        width="52px",
                        cursor=rx.cond(LearnState.typed_answer != "", "pointer", "not-allowed"),
                    ),
                    width="100%",
                    spacing="2",
                ),
                spacing="2",
                width="100%",
            ),
        ),
        spacing="4",
        width="100%",
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE: CHOICE (Multiple choice)
# ═══════════════════════════════════════════════════════════════════

def _choice_button(option: str):
    is_selected = LearnState.selected_answer == option
    is_correct = LearnState.correct_answer == option
    has_answered = LearnState.selected_answer != ""

    bg = rx.cond(
        has_answered,
        rx.cond(is_correct, "#DCFCE7", rx.cond(is_selected, "#FEE2E2", "white")),
        "white",
    )
    border = rx.cond(
        has_answered,
        rx.cond(is_correct, "2px solid #16A34A", rx.cond(is_selected, "2px solid #DC2626", "1.5px solid #E5E7EB")),
        rx.cond(is_selected, "2px solid #4F46E5", "1.5px solid #E5E7EB"),
    )
    text_color = rx.cond(
        has_answered,
        rx.cond(is_correct, "#15803D", rx.cond(is_selected, "#B91C1C", "#9CA3AF")),
        "#111827",
    )

    return rx.box(
        rx.hstack(
            rx.text(option, font_size="1rem", font_weight="600", color=text_color, flex="1"),
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
        width="100%",
        padding="0.9rem 1.2rem",
        border=border,
        border_radius="14px",
        bg=bg,
        cursor=rx.cond(has_answered, "default", "pointer"),
        on_click=lambda: LearnState.select_choice(option),
        _hover=rx.cond(has_answered, {}, {"bg": "#F5F3FF", "border_color": "#4F46E5"}),
        transition="all 0.15s ease",
    )


def choice_phase():
    return rx.vstack(
        # Question
        rx.box(
            rx.vstack(
                rx.text("Nghĩa", font_size="0.78rem", font_weight="700", color="#9CA3AF",
                        text_transform="uppercase", letter_spacing="0.08em"),
                rx.text(LearnState.current_card_front, font_size="1.5rem", font_weight="700",
                        color="#111827", text_align="center", line_height="1.3"),
                spacing="2", align="center",
            ),
            width="100%",
            padding="1.5rem",
            bg="#FFFBEB",
            border="1.5px solid #FDE68A",
            border_radius="16px",
            text_align="center",
        ),

        rx.text("Chọn thuật ngữ đúng", font_size="0.82rem", color="#6B7280", font_weight="500"),

        # 4 options
        rx.grid(
            rx.foreach(LearnState.choice_options, _choice_button),
            template_columns="repeat(2, minmax(0, 1fr))",
            gap="3",
            width="100%",
        ),

        # Continue button after answering
        rx.cond(
            LearnState.show_feedback,
            rx.button(
                "Tiếp theo →",
                on_click=LearnState.continue_after_choice,
                bg=rx.cond(LearnState.feedback_correct, "#16A34A", "#DC2626"),
                color="white",
                border_radius="12px",
                padding="0.65rem 2rem",
                font_weight="700",
                width="100%",
                _hover={"opacity": "0.9"},
            ),
            rx.box(),
        ),

        spacing="4",
        width="100%",
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE: REVIEW SUMMARY (giữa các vòng)
# ═══════════════════════════════════════════════════════════════════

def review_summary_phase():
    return rx.vstack(
        rx.vstack(
            rx.icon("refresh-cw", size=40, color="#F59E0B"),
            rx.text(
                "Ôn lại vòng ", LearnState.round_number,
                font_size="1.5rem", font_weight="700", color="#111827",
            ),
            rx.text(
                "Bạn vẫn còn một số thẻ cần luyện thêm. Hãy tiếp tục!",
                font_size="0.95rem", color="#6B7280", text_align="center",
            ),
            spacing="3", align="center",
        ),
        rx.hstack(
            rx.vstack(
                rx.text(LearnState.total_correct, font_size="2rem", font_weight="800", color="#16A34A"),
                rx.text("Đúng", font_size="0.85rem", color="#6B7280"),
                align="center",
            ),
            rx.box(width="1px", height="50px", bg="#E5E7EB"),
            rx.vstack(
                rx.text(LearnState.total_wrong, font_size="2rem", font_weight="800", color="#DC2626"),
                rx.text("Sai", font_size="0.85rem", color="#6B7280"),
                align="center",
            ),
            rx.box(width="1px", height="50px", bg="#E5E7EB"),
            rx.vstack(
                rx.text(LearnState.mastered_count, font_size="2rem", font_weight="800", color="#4F46E5"),
                rx.text("Thành thạo", font_size="0.85rem", color="#6B7280"),
                align="center",
            ),
            spacing="6", justify="center", width="100%",
        ),
        rx.button(
            "Tiếp tục luyện tập →",
            on_click=LearnState.continue_review_round,
            bg="#F59E0B",
            color="white",
            border_radius="14px",
            padding="0.9rem 2rem",
            font_weight="700",
            font_size="1rem",
            width="100%",
            _hover={"bg": "#D97706"},
        ),
        spacing="6",
        align="center",
        padding_y="1rem",
        width="100%",
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE: COMPLETE
# ═══════════════════════════════════════════════════════════════════

def complete_phase():
    return rx.vstack(
        rx.vstack(
            rx.text("🎉", font_size="3.5rem"),
            rx.text(
                "Xuất sắc!",
                font_size="1.8rem", font_weight="800", color="#111827",
            ),
            rx.text(
                "Bạn đã thành thạo toàn bộ học phần này!",
                font_size="1rem", color="#6B7280", text_align="center",
            ),
            spacing="2", align="center",
        ),
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text(LearnState.accuracy_pct, "%", font_size="2.2rem", font_weight="800",
                            color=rx.cond(LearnState.accuracy_pct >= 70, "#16A34A", "#F59E0B")),
                    rx.text("Độ chính xác", font_size="0.8rem", color="#6B7280"),
                    align="center",
                ),
                rx.box(width="1px", height="60px", bg="#E5E7EB"),
                rx.vstack(
                    rx.text(LearnState.mastered_count, font_size="2.2rem", font_weight="800", color="#4F46E5"),
                    rx.text("Thành thạo", font_size="0.8rem", color="#6B7280"),
                    align="center",
                ),
                rx.box(width="1px", height="60px", bg="#E5E7EB"),
                rx.vstack(
                    rx.text(LearnState.round_number, font_size="2.2rem", font_weight="800", color="#F59E0B"),
                    rx.text("Vòng học", font_size="0.8rem", color="#6B7280"),
                    align="center",
                ),
                spacing="6", justify="center", width="100%",
            ),
            bg="#F8FAFC",
            border="1.5px solid #E5E7EB",
            border_radius="16px",
            padding="1.5rem",
            width="100%",
        ),
        rx.hstack(
            rx.button(
                rx.hstack(rx.icon("refresh-cw", size=16), rx.text("Học lại"), spacing="2"),
                on_click=LearnState.close_learn,
                bg="white",
                color="#4F46E5",
                border="2px solid #4F46E5",
                border_radius="12px",
                padding="0.75rem 1.5rem",
                font_weight="700",
                _hover={"bg": "#EEF2FF"},
                flex="1",
            ),
            rx.button(
                rx.hstack(rx.icon("x", size=16), rx.text("Đóng"), spacing="2"),
                on_click=LearnState.close_learn,
                bg="#4F46E5",
                color="white",
                border_radius="12px",
                padding="0.75rem 1.5rem",
                font_weight="700",
                _hover={"bg": "#4338CA"},
                flex="1",
            ),
            spacing="3", width="100%",
        ),
        spacing="6", align="center", width="100%",
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE ROUTER
# ═══════════════════════════════════════════════════════════════════

def learn_phase_router():
    return rx.cond(
        LearnState.phase == "preview",
        preview_phase(),
        rx.cond(
            LearnState.phase == "type",
            type_phase(),
            rx.cond(
                LearnState.phase == "choice",
                choice_phase(),
                rx.cond(
                    LearnState.phase == "review",
                    review_summary_phase(),
                    complete_phase(),
                ),
            ),
        ),
    )


# ═══════════════════════════════════════════════════════════════════
# MAIN OVERLAY
# ═══════════════════════════════════════════════════════════════════

def learn_overlay():
    """Full-screen overlay cho chế độ Học."""
    return rx.cond(
        LearnState.show_learn,
        rx.box(
            rx.box(
                rx.vstack(
                    # ── Header ──────────────────────────────────────
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                LearnState.set_title,
                                font_size="1.15rem",
                                font_weight="700",
                                color="#111827",
                            ),
                            rx.hstack(
                                _phase_badge(),
                                rx.text(
                                    LearnState.queue_progress_label,
                                    font_size="0.8rem",
                                    color="#6B7280",
                                    font_weight="600",
                                ),
                                spacing="2",
                                align="center",
                            ),
                            spacing="1",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon("x", size=18),
                            on_click=LearnState.close_learn,
                            bg="transparent",
                            color="#6B7280",
                            border_radius="8px",
                            padding="0.4rem",
                            _hover={"bg": "#F3F4F6"},
                        ),
                        width="100%",
                        align="center",
                    ),

                    # ── Progress ────────────────────────────────────
                    rx.cond(
                        LearnState.phase != "complete",
                        _progress_bar(),
                        rx.box(),
                    ),

                    rx.divider(),

                    # ── Phase content ───────────────────────────────
                    learn_phase_router(),

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
            display="flex",
            align_items="center",
            justify_content="center",
            bg="rgba(17,24,39,0.45)",
            z_index="1000",
            padding="1.5rem",
            on_click=LearnState.close_learn,
        ),
        rx.box(),
    )