import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.learn_state import LearnState


# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════

def _progress_bar():
    return rx.vstack(
        rx.hstack(
            rx.hstack(
                rx.box(width="10px", height="10px", border_radius="999px", bg="#16A34A"),
                rx.text(LearnState.mastered_count, " thành thạo",
                        font_size="0.78rem", color="#16A34A", font_weight="600"),
                spacing="1", align="center",
            ),
            rx.hstack(
                rx.box(width="10px", height="10px", border_radius="999px", bg="#F59E0B"),
                rx.text(LearnState.learning_count, " đang học",
                        font_size="0.78rem", color="#F59E0B", font_weight="600"),
                spacing="1", align="center",
            ),
            rx.hstack(
                rx.box(width="10px", height="10px", border_radius="999px", bg="#E5E7EB"),
                rx.text(LearnState.not_started_count, " chưa học",
                        font_size="0.78rem", color="#9CA3AF", font_weight="600"),
                spacing="1", align="center",
            ),
            spacing="5",
        ),
        rx.box(
            rx.box(
                height="100%",
                width=LearnState.batch_progress_pct.to_string() + "%",
                bg=f"linear-gradient(90deg, {T.PRIMARY}, #5B8CFF)",
                border_radius="999px",
                transition="width 0.4s ease",
            ),
            width="100%", height="8px", bg=T.BORDER_LIGHT, border_radius="999px", overflow="hidden",
        ),
        rx.box(
            rx.box(
                height="100%",
                width=LearnState.total_progress_pct.to_string() + "%",
                bg="linear-gradient(90deg, #16A34A, #22C55E)",
                border_radius="999px",
                transition="width 0.6s ease",
            ),
            width="100%", height="4px", bg=T.BORDER_LIGHT, border_radius="999px", overflow="hidden",
        ),
        width="100%", spacing="2",
    )


def _phase_badge():
    label = rx.cond(
        LearnState.phase == "preview", "Xem thẻ mới",
        rx.cond(
            LearnState.phase == "practice",
            rx.cond(LearnState.current_practice_mode == "type", "Gõ đáp án", "Trắc nghiệm"),
            rx.cond(
                LearnState.phase == "batch_review", "Ôn lô",
                rx.cond(LearnState.phase == "round_review", "Ôn vòng", "Hoàn thành"),
            ),
        ),
    )
    bg = rx.cond(
        LearnState.phase == "preview", "#E0F2FE",
        rx.cond(
            LearnState.phase == "practice",
            rx.cond(LearnState.current_practice_mode == "type", "#EDE9FE", "#FEF3C7"),
            "#FCE7F3",
        ),
    )
    color = rx.cond(
        LearnState.phase == "preview", "#0369A1",
        rx.cond(
            LearnState.phase == "practice",
            rx.cond(LearnState.current_practice_mode == "type", "#6D28D9", "#B45309"),
            "#BE185D",
        ),
    )
    return rx.box(
        rx.text(label, font_size="0.75rem", font_weight="700", color=color),
        bg=bg, border_radius="999px", padding="0.25rem 0.75rem",
    )


def _new_tag():
    return rx.cond(
        LearnState.current_item_is_new,
        rx.box(
            rx.text("MỚI", font_size="0.65rem", font_weight="800", color="#0369A1",
                    letter_spacing="0.08em"),
            bg="#E0F2FE", border_radius="999px", padding="0.15rem 0.5rem",
        ),
        rx.box(),
    )


def _direction_toggle():
    is_ntf = LearnState.answer_language == "native_to_foreign"
    return rx.hstack(
        rx.text("Hỏi:", font_size="0.7rem", font_weight="500", color=T.TEXT_MUTED),
        rx.hstack(
            rx.box(
                rx.text("F", font_size="0.7rem", font_weight="500",
                        color=rx.cond(is_ntf, "white", T.TEXT_MUTED),
                        white_space="nowrap"),
                padding="3px 8px",
                border_radius="999px",
                bg=rx.cond(is_ntf, T.PRIMARY, "transparent"),
                cursor="pointer",
                on_click=lambda: LearnState.set_answer_language("native_to_foreign"),
                transition="all 0.15s ease",
            ),
            rx.box(
                rx.text("N", font_size="0.7rem", font_weight="500",
                        color=rx.cond(~is_ntf, "white", T.TEXT_MUTED),
                        white_space="nowrap"),
                padding="3px 8px",
                border_radius="999px",
                bg=rx.cond(~is_ntf, T.PRIMARY, "transparent"),
                cursor="pointer",
                on_click=lambda: LearnState.set_answer_language("foreign_to_native"),
                transition="all 0.15s ease",
            ),
            spacing="0",
            bg=T.BORDER_LIGHT,
            border=f"0.5px solid {T.BORDER}",
            border_radius="999px",
            padding="2px",
        ),
        spacing="2",
        align="center",
    )

# ═══════════════════════════════════════════════════════════════════
# PHASE: PREVIEW
# ═══════════════════════════════════════════════════════════════════

def preview_phase():
    return rx.vstack(
        rx.hstack(
            rx.box(
                rx.text(LearnState.batch_label,
                        font_size="0.72rem", font_weight="700", color=T.PRIMARY),
                bg=T.PRIMARY_TINT, border_radius="999px", padding="0.2rem 0.7rem",
            ),
            rx.text(LearnState.batch_composition_label,
                    font_size="0.78rem", color="#9CA3AF"),
            spacing="2", align="center",
        ),

        rx.box(
            rx.vstack(
                rx.text(
                    rx.cond(
                        LearnState.is_preview_flipped,
                        LearnState.answer_label,
                        LearnState.prompt_label,
                    ),
                    font_size="0.78rem", font_weight="700", color=T.PRIMARY,
                    text_transform="uppercase", letter_spacing="0.08em",
                ),
                rx.text(
                    rx.cond(
                        LearnState.is_preview_flipped,
                        LearnState.current_card_back,
                        LearnState.current_card_front,
                    ),
                    font_size="2rem", font_weight="700", color=T.TEXT_PRIMARY,
                    text_align="center", line_height="1.3",
                ),
                rx.text("Nhấp để lật thẻ", font_size="0.75rem", color=T.TEXT_SECONDARY,
                        margin_top="0.5rem"),
                spacing="3", align="center", justify="center", height="100%",
            ),
            width="100%", min_height="200px",
            bg=T.LEARN_CARD_BG,
            border=f"2px solid {T.LEARN_CARD_BORDER}", border_radius="20px",
            padding="2rem", cursor="pointer",
            on_click=LearnState.flip_preview,
            display="flex", align_items="center", justify_content="center",
            transition="all 0.2s ease",
            _hover={"border_color": T.PRIMARY, "box_shadow": T.SHADOW_CARD_HOVER},
        ),

        rx.hstack(
            rx.button(
                rx.hstack(rx.icon("rotate-ccw", size=16), rx.text("Vẫn đang học"),
                          spacing="2", align="center"),
                on_click=LearnState.preview_still_learning,
                bg="white", color="#374151",
                border="2px solid #E5E7EB", border_radius="12px",
                padding="0.75rem 1.5rem", font_weight="600",
                _hover={"bg": "#F9FAFB", "border_color": "#D1D5DB"},
                flex="1",
            ),
            rx.button(
                rx.hstack(rx.icon("check", size=16), rx.text("Đã biết"),
                          spacing="2", align="center"),
                on_click=LearnState.preview_got_it,
                bg=T.PRIMARY, color="white",
                border_radius="12px", padding="0.75rem 1.5rem", font_weight="600",
                _hover={"bg": T.PRIMARY_HOVER},
                flex="1",
            ),
            spacing="3", width="100%",
        ),
        spacing="4", width="100%",
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE: PRACTICE — TYPE
# ═══════════════════════════════════════════════════════════════════

def _question_box(accent_bg: str, accent_border: str):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    LearnState.prompt_label,  # ← dùng computed var thay vì hardcode "Nghĩa"
                    font_size="0.78rem", font_weight="700", color="#9CA3AF",
                    text_transform="uppercase", letter_spacing="0.08em",
                ),
                _new_tag(),
                spacing="2", align="center",
            ),
            rx.text(LearnState.current_card_front, font_size="1.5rem", font_weight="700",
                    color="#111827", text_align="center", line_height="1.3"),
            spacing="2", align="center",
        ),
        width="100%", padding="1.5rem",
        bg=accent_bg, border=f"1.5px solid {accent_border}",
        border_radius="16px", text_align="center",
    )


def type_practice():
    return rx.vstack(
        _question_box(T.QUESTION_BOX_BG, T.QUESTION_BOX_BORDER),
        rx.cond(
            LearnState.show_feedback,
            rx.vstack(
                rx.box(
                    rx.text(LearnState.feedback_message, font_size="1rem", font_weight="600",
                            text_align="center",
                            color=rx.cond(LearnState.feedback_correct, "#15803D", "#B91C1C")),
                    width="100%", padding="1rem 1.2rem",
                    bg=rx.cond(LearnState.feedback_correct, "#F0FDF4", "#FFF5F5"),
                    border=rx.cond(LearnState.feedback_correct,
                                   "1.5px solid #BBF7D0", "1.5px solid #FECACA"),
                    border_radius="14px",
                ),
                rx.button(
                    "Tiếp theo →",
                    on_click=LearnState.continue_after_type,
                    bg=rx.cond(LearnState.feedback_correct, "#16A34A", "#DC2626"),
                    color="white", border_radius="12px",
                    padding="0.65rem 1.5rem", font_weight="700", width="100%",
                    _hover={"opacity": "0.9"},
                ),
                spacing="3", width="100%",
            ),
            rx.vstack(
                rx.text(
                    rx.cond(
                        LearnState.answer_language == "native_to_foreign",
                        "Gõ thuật ngữ",
                        "Gõ nghĩa",
                    ),
                    font_size="0.85rem", color="#6B7280", font_weight="500",
                ),
                rx.hstack(
                    rx.input(
                        value=LearnState.typed_answer,
                        on_change=LearnState.set_typed_answer,
                        placeholder="Nhập đáp án...",
                        width="100%", height="52px",
                        bg="white", border="2px solid #E5E7EB", border_radius="12px",
                        font_size="1.05rem", padding="0 1rem",
                        _focus={"border_color": T.PRIMARY,
                                "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}"},
                    ),
                    rx.button(
                        rx.icon("send", size=18),
                        on_click=LearnState.submit_typed,
                        bg=rx.cond(LearnState.typed_answer != "", T.PRIMARY, T.PRIMARY_DISABLED),
                        color="white", border_radius="12px", height="52px", width="52px",
                        cursor=rx.cond(LearnState.typed_answer != "", "pointer", "not-allowed"),
                    ),
                    width="100%", spacing="2",
                ),
                spacing="2", width="100%",
            ),
        ),
        spacing="4", width="100%",
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE: PRACTICE — CHOICE
# ═══════════════════════════════════════════════════════════════════

def _choice_btn(option: str):
    is_selected = LearnState.selected_answer == option
    is_correct = LearnState.correct_answer == option
    has_answered = LearnState.selected_answer != ""

    return rx.box(
        rx.hstack(
            rx.text(option, font_size="0.97rem", font_weight="600", flex="1",
                    color=rx.cond(
                        has_answered,
                        rx.cond(is_correct, "#15803D",
                                rx.cond(is_selected, "#B91C1C", "#9CA3AF")),
                        "#111827",
                    )),
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
            rx.cond(is_selected, f"2px solid {T.PRIMARY}", f"1.5px solid {T.BORDER}"),
        ),
        border_radius="13px",
        bg=rx.cond(
            has_answered,
            rx.cond(is_correct, "#DCFCE7",
                    rx.cond(is_selected, "#FEE2E2", "white")),
            "white",
        ),
        cursor=rx.cond(has_answered, "default", "pointer"),
        on_click=lambda: LearnState.select_choice(option),
        _hover=rx.cond(has_answered, {}, {"bg": T.PRIMARY_TINT, "border_color": T.PRIMARY}),
        transition="all 0.14s ease",
    )


def choice_practice():
    return rx.vstack(
        _question_box(T.QUESTION_BOX_ALT_BG, T.QUESTION_BOX_ALT_BORDER),
        rx.text(
            rx.cond(
                LearnState.answer_language == "native_to_foreign",
                "Chọn thuật ngữ đúng",
                "Chọn nghĩa đúng",
            ),
            font_size="0.82rem", color="#6B7280", font_weight="500",
        ),
        rx.grid(
            rx.foreach(LearnState.choice_options, _choice_btn),
            template_columns="repeat(2, minmax(0, 1fr))",
            gap="3", width="100%",
        ),
        rx.cond(
            LearnState.show_feedback,
            rx.button(
                "Tiếp theo →",
                on_click=LearnState.continue_after_choice,
                bg=rx.cond(LearnState.feedback_correct, "#16A34A", "#DC2626"),
                color="white", border_radius="12px",
                padding="0.65rem 2rem", font_weight="700", width="100%",
                _hover={"opacity": "0.9"},
            ),
            rx.box(),
        ),
        spacing="4", width="100%",
    )


def practice_phase():
    return rx.cond(
        LearnState.current_practice_mode == "type",
        type_practice(),
        choice_practice(),
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE: BATCH REVIEW
# ═══════════════════════════════════════════════════════════════════

def batch_review_phase():
    return rx.vstack(
        rx.hstack(
            rx.icon("alert-triangle", size=20, color="#F59E0B"),
            rx.vstack(
                rx.text("Ôn lại thẻ sai trong lô",
                        font_size="1rem", font_weight="700", color="#111827"),
                rx.text("Gõ lại để ghi nhớ chắc hơn trước khi sang lô tiếp.",
                        font_size="0.82rem", color="#6B7280"),
                spacing="0", align="start",
            ),
            spacing="3", align="start",
            padding="1rem 1.2rem",
            bg="#FFFBEB", border="1.5px solid #FDE68A", border_radius="14px",
            width="100%",
        ),
        type_practice(),
        spacing="4", width="100%",
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE: ROUND REVIEW
# ═══════════════════════════════════════════════════════════════════

def round_review_phase():
    return rx.vstack(
        rx.vstack(
            rx.icon("refresh-cw", size=40, color="#F59E0B"),
            rx.text("Kết thúc vòng ", LearnState.round_number,
                    font_size="1.5rem", font_weight="700", color="#111827"),
            rx.text("Vẫn còn thẻ chưa thành thạo. Tiếp tục ôn lại!",
                    font_size="0.9rem", color="#6B7280", text_align="center"),
            spacing="3", align="center",
        ),
        rx.hstack(
            rx.vstack(
                rx.text(LearnState.total_correct, font_size="2rem", font_weight="800",
                        color="#16A34A"),
                rx.text("Đúng", font_size="0.85rem", color="#6B7280"),
                align="center",
            ),
            rx.box(width="1px", height="50px", bg="#E5E7EB"),
            rx.vstack(
                rx.text(LearnState.total_wrong, font_size="2rem", font_weight="800",
                        color="#DC2626"),
                rx.text("Sai", font_size="0.85rem", color="#6B7280"),
                align="center",
            ),
            rx.box(width="1px", height="50px", bg="#E5E7EB"),
            rx.vstack(
                rx.text(LearnState.mastered_count, font_size="2rem", font_weight="800",
                        color=T.PRIMARY),
                rx.text("Thành thạo", font_size="0.85rem", color="#6B7280"),
                align="center",
            ),
            spacing="6", justify="center", width="100%",
        ),
        rx.button(
            "Ôn lại vòng mới →",
            on_click=LearnState.continue_round_review,
            bg="#F59E0B", color="white", border_radius="14px",
            padding="0.9rem 2rem", font_weight="700", font_size="1rem",
            width="100%", _hover={"bg": "#D97706"},
        ),
        spacing="6", align="center", padding_y="1rem", width="100%",
    )


# ═══════════════════════════════════════════════════════════════════
# PHASE: COMPLETE
# ═══════════════════════════════════════════════════════════════════

def complete_phase():
    return rx.vstack(
        rx.vstack(
            rx.text("🎉", font_size="3.5rem"),
            rx.text("Xuất sắc!", font_size="1.8rem", font_weight="800", color="#111827"),
            rx.text("Bạn đã thành thạo toàn bộ học phần này!",
                    font_size="1rem", color="#6B7280", text_align="center"),
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
                    rx.text(LearnState.mastered_count, font_size="2.2rem", font_weight="800",
                            color=T.PRIMARY),
                    rx.text("Thành thạo", font_size="0.8rem", color="#6B7280"),
                    align="center",
                ),
                rx.box(width="1px", height="60px", bg="#E5E7EB"),
                rx.vstack(
                    rx.text(LearnState.round_number, font_size="2.2rem", font_weight="800",
                            color="#F59E0B"),
                    rx.text("Vòng học", font_size="0.8rem", color="#6B7280"),
                    align="center",
                ),
                spacing="6", justify="center", width="100%",
            ),
            bg="#F8FAFC", border="1.5px solid #E5E7EB",
            border_radius="16px", padding="1.5rem", width="100%",
        ),
        rx.hstack(
            rx.button(
                rx.hstack(rx.icon("refresh-cw", size=16), rx.text("Học lại"), spacing="2"),
                on_click=LearnState.close_learn,
                bg="white", color=T.PRIMARY,
                border=f"2px solid {T.PRIMARY}", border_radius="12px",
                padding="0.75rem 1.5rem", font_weight="700",
                _hover={"bg": T.PRIMARY_TINT}, flex="1",
            ),
            rx.button(
                rx.hstack(rx.icon("x", size=16), rx.text("Đóng"), spacing="2"),
                on_click=LearnState.close_learn,
                bg=T.PRIMARY, color="white", border_radius="12px",
                padding="0.75rem 1.5rem", font_weight="700",
                _hover={"bg": T.PRIMARY_HOVER}, flex="1",
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
            LearnState.phase == "practice",
            practice_phase(),
            rx.cond(
                LearnState.phase == "batch_review",
                batch_review_phase(),
                rx.cond(
                    LearnState.phase == "round_review",
                    round_review_phase(),
                    complete_phase(),
                ),
            ),
        ),
    )


# ═══════════════════════════════════════════════════════════════════
# MAIN OVERLAY
# ═══════════════════════════════════════════════════════════════════

def learn_overlay():
    return rx.cond(
        LearnState.show_learn,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.text(LearnState.set_title,
                                    font_size="1.15rem", font_weight="700", color=T.TEXT_PRIMARY),
                            rx.hstack(
                                _phase_badge(),
                                rx.text(LearnState.queue_progress_label,
                                        font_size="0.8rem", color="#6B7280", font_weight="600"),
                                rx.text("·", color="#D1D5DB"),
                                rx.text(LearnState.batch_label,
                                        font_size="0.8rem", color=T.PRIMARY, font_weight="700"),
                                spacing="2", align="center",
                            ),
                            rx.cond(
                                LearnState.phase == "practice",
                                rx.text(
                                    LearnState.session_srs_hint,
                                    font_size="0.72rem",
                                    color=T.TEXT_SECONDARY,
                                    line_height="1.35",
                                ),
                                rx.cond(
                                    LearnState.phase == "batch_review",
                                    rx.text(
                                        LearnState.session_srs_hint,
                                        font_size="0.72rem",
                                        color=T.TEXT_SECONDARY,
                                        line_height="1.35",
                                    ),
                                    rx.box(),
                                ),
                            ),
                            spacing="1", align="start",
                        ),
                        rx.spacer(),
                        # ── Toggle hướng hỏi-đáp ──────────────
                        rx.cond(
                            LearnState.phase != "complete",
                            _direction_toggle(),
                            rx.box(),
                        ),
                        rx.button(
                            rx.icon("x", size=18),
                            on_click=LearnState.close_learn,
                            bg="transparent", color="#6B7280",
                            border_radius="8px", padding="0.4rem",
                            _hover={"bg": "#F3F4F6"},
                        ),
                        width="100%", align="center", spacing="3",
                    ),

                    # Progress bars
                    rx.cond(
                        LearnState.phase != "complete",
                        _progress_bar(),
                        rx.box(),
                    ),

                    rx.divider(),

                    learn_phase_router(),

                    spacing="5", padding="1.8rem 2rem 2rem", width="100%",
                ),
                bg="white", border_radius=T.RADIUS_XL,
                width="580px", max_width="min(580px, calc(100vw - 2.5rem))",
                max_height=T.MODAL_CONTENT_MAX_HEIGHT,
                min_height="0",
                overflow_y="auto",
                overflow_x="hidden",
                border=f"1px solid {T.BORDER}",
                box_shadow=T.SHADOW_MODAL,
                on_click=rx.stop_propagation,
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg=T.OVERLAY_SCRIM, z_index="1000", padding=T.MODAL_OVERLAY_PADDING,
            on_click=LearnState.close_learn,
        ),
        rx.box(),
    )