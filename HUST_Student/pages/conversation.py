import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.models.conversation import ChatLine
from HUST_Student.states.conversation_state import ConversationState

_LANGS = ["vi", "en", "ja", "ko", "zh", "fr", "de", "es", "it", "pt", "ru"]
_LEVELS = ["beginner", "intermediate", "advanced"]


def _level_label_var(level_state):
    return rx.cond(
        level_state == "beginner",
        "Cơ bản",
        rx.cond(level_state == "intermediate", "Trung cấp", "Nâng cao"),
    )


def _chat_bubble(row: ChatLine):
    role = row.role
    is_user = role == "user"
    is_feedback = role == "feedback"
    bg = rx.cond(
        is_user,
        T.PRIMARY_TINT,
        rx.cond(is_feedback, T.BORDER_LIGHT, T.SURFACE),
    )
    border = rx.cond(
        is_user,
        f"1px solid {T.PRIMARY}",
        rx.cond(is_feedback, f"1px solid {T.WARN}", f"1px solid {T.BORDER}"),
    )
    return rx.box(
        rx.text(
            row.text,
            font_size="0.95rem",
            color=T.TEXT_PRIMARY,
            white_space="pre-wrap",
            line_height="1.5",
        ),
        align_self=rx.cond(is_user, "flex-end", "flex-start"),
        max_width="min(92%, 560px)",
        padding="0.85rem 1.1rem",
        border_radius=T.RADIUS_LG,
        bg=bg,
        border=border,
        box_shadow=T.SHADOW_CARD,
    )


def conversation_page():
    return rx.vstack(
        rx.text(
            "Luyện hội thoại",
            font_size="2rem",
            font_weight="800",
            color=T.TEXT_PRIMARY,
            letter_spacing="-0.02em",
        ),
        rx.text(
            "Chọn ngôn ngữ nguồn (bản xứ) và ngôn ngữ đích, cùng cấp độ cho từng phía. "
            "Cụm giao tiếp chỉ được tải từ API Internet (bắt buộc cấu hình HUST_CONVERSATION_API_URL).",
            font_size="0.95rem",
            color=T.TEXT_SECONDARY,
            max_width="48rem",
        ),
        rx.box(
            rx.vstack(
                rx.text("Thiết lập phiên", font_weight="700", color=T.TEXT_PRIMARY),
                rx.hstack(
                    rx.vstack(
                        rx.text("Ngôn ngữ bản xứ (native)", font_size="0.8rem", color=T.TEXT_SECONDARY),
                        rx.select(
                            _LANGS,
                            value=ConversationState.native_lang,
                            on_change=ConversationState.set_native_lang,
                            width="140px",
                            border=f"1px solid {T.BORDER}",
                            border_radius=T.RADIUS_MD,
                        ),
                        rx.text(
                            "Cấp độ (native)",
                            font_size="0.8rem",
                            color=T.TEXT_SECONDARY,
                            margin_top="0.35rem",
                        ),
                        rx.select(
                            _LEVELS,
                            value=ConversationState.native_level,
                            on_change=ConversationState.set_native_level,
                            width="140px",
                            border=f"1px solid {T.BORDER}",
                            border_radius=T.RADIUS_MD,
                        ),
                        rx.text(
                            _level_label_var(ConversationState.native_level),
                            font_size="0.72rem",
                            color=T.TEXT_MUTED,
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Ngôn ngữ đích (foreign)", font_size="0.8rem", color=T.TEXT_SECONDARY),
                        rx.select(
                            _LANGS,
                            value=ConversationState.foreign_lang,
                            on_change=ConversationState.set_foreign_lang,
                            width="140px",
                            border=f"1px solid {T.BORDER}",
                            border_radius=T.RADIUS_MD,
                        ),
                        rx.text(
                            "Cấp độ (foreign)",
                            font_size="0.8rem",
                            color=T.TEXT_SECONDARY,
                            margin_top="0.35rem",
                        ),
                        rx.select(
                            _LEVELS,
                            value=ConversationState.foreign_level,
                            on_change=ConversationState.set_foreign_level,
                            width="140px",
                            border=f"1px solid {T.BORDER}",
                            border_radius=T.RADIUS_MD,
                        ),
                        rx.text(
                            _level_label_var(ConversationState.foreign_level),
                            font_size="0.72rem",
                            color=T.TEXT_MUTED,
                        ),
                        spacing="1",
                        align="start",
                    ),
                    spacing="6",
                    flex_wrap="wrap",
                    width="100%",
                ),
                rx.hstack(
                    rx.button(
                        "Tải câu & bắt đầu",
                        on_click=ConversationState.load_lesson,
                        bg=T.PRIMARY,
                        color="white",
                        border_radius=T.RADIUS_PILL,
                        font_weight="700",
                        padding_x="1.5rem",
                        _hover={"bg": T.PRIMARY_HOVER},
                    ),
                    rx.cond(
                        ConversationState.loading,
                        rx.text("Đang tải…", color=T.PRIMARY, font_weight="600"),
                        rx.box(),
                    ),
                    spacing="4",
                    align="center",
                ),
                rx.cond(
                    ConversationState.show_error_banner,
                    rx.text(
                        ConversationState.error,
                        color=T.DANGER,
                        font_size="0.88rem",
                        font_weight="600",
                    ),
                    rx.box(),
                ),
                rx.cond(
                    ConversationState.show_source_banner,
                    rx.text(
                        ConversationState.source_badge,
                        font_size="0.82rem",
                        color=T.TEXT_MUTED,
                        font_weight="500",
                    ),
                    rx.box(),
                ),
                spacing="4",
                align="start",
                width="100%",
            ),
            width="100%",
            max_width="720px",
            padding="1.25rem 1.5rem",
            border_radius=T.RADIUS_XL,
            border=f"1px solid {T.BORDER}",
            bg=T.SURFACE,
            box_shadow=T.SHADOW_CARD,
        ),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("Khung chat luyện tập", font_weight="700", color=T.TEXT_PRIMARY),
                    rx.spacer(),
                    spacing="2",
                    width="100%",
                ),
                rx.box(
                    rx.vstack(
                        rx.foreach(ConversationState.chat_rows, _chat_bubble),
                        spacing="3",
                        width="100%",
                        align="stretch",
                    ),
                    min_height="280px",
                    max_height="420px",
                    overflow_y="auto",
                    padding="1rem",
                    width="100%",
                    border_radius=T.RADIUS_LG,
                    bg=T.PAGE_BG,
                    border=f"1px solid {T.BORDER_LIGHT}",
                ),
                rx.input(
                    placeholder="Nhập câu trả lời của bạn (tiếng đích)…",
                    value=ConversationState.user_input,
                    on_change=ConversationState.set_user_input,
                    size="3",
                    width="100%",
                    border=f"1px solid {T.BORDER}",
                    border_radius=T.RADIUS_MD,
                    padding="0.85rem 1rem",
                ),
                rx.button(
                    "Gửi",
                    on_click=ConversationState.submit_answer,
                    width="100%",
                    bg=T.PRIMARY,
                    color="white",
                    font_weight="700",
                    border_radius=T.RADIUS_PILL,
                    _hover={"bg": T.PRIMARY_HOVER},
                ),
                spacing="4",
                width="100%",
            ),
            width="100%",
            max_width="720px",
            padding="1.25rem 1.5rem",
            border_radius=T.RADIUS_XL,
            border=f"1px solid {T.BORDER}",
            bg=T.SURFACE,
            box_shadow=T.SHADOW_CARD,
        ),
        rx.text(
            "Bắt buộc: biến môi trường HUST_CONVERSATION_API_URL (base URL). "
            "GET {base}/phrases?… — JSON {\"phrases\": [{\"native\",\"foreign\",…}]}.",
            font_size="0.78rem",
            color=T.TEXT_MUTED,
            max_width="720px",
        ),
        spacing="6",
        align="start",
        width="100%",
        padding_top="0.5rem",
    )
