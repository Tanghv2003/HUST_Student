import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.models.conversation import ChatLine
from HUST_Student.states.conversation_state import ConversationState

_LANG_CODES = ["vi", "en", "ja", "ko", "zh", "fr", "de", "es", "it", "pt", "ru"]
_LEVELS = ["beginner", "intermediate", "advanced"]


def _chat_bubble(row: ChatLine):
    is_user = row.role == "user"

    return rx.box(
        rx.cond(
            is_user,
            # User bubble — right aligned
            rx.hstack(
                rx.spacer(),
                rx.box(
                    rx.text(
                        row.text,
                        font_size="0.925rem",
                        color="white",
                        white_space="pre-wrap",
                        line_height="1.6",
                    ),
                    padding="0.85rem 1.1rem",
                    border_radius="18px 18px 4px 18px",
                    bg=T.PRIMARY,
                    box_shadow=T.SHADOW_CARD,
                    max_width="min(86%, 520px)",
                ),
                width="100%",
                align="start",
            ),
            # Tutor bubble — left aligned
            rx.hstack(
                rx.box(
                    rx.text("AI", font_size="0.65rem", font_weight="800", color="white"),
                    bg=T.PRIMARY,
                    border_radius="999px",
                    width="28px",
                    height="28px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                    margin_top="2px",
                ),
                rx.box(
                    rx.text(
                        row.text,
                        font_size="0.925rem",
                        color=T.TEXT_PRIMARY,
                        white_space="pre-wrap",
                        line_height="1.6",
                    ),
                    padding="0.85rem 1.1rem",
                    border_radius="18px 18px 18px 4px",
                    bg=T.SURFACE,
                    border=f"1px solid {T.BORDER}",
                    box_shadow=T.SHADOW_CARD,
                    max_width="min(86%, 520px)",
                ),
                width="100%",
                align="start",
                spacing="2",
            ),
        ),
        width="100%",
        padding_x="0.25rem",
    )


def conversation_page():
    return rx.vstack(
        # ── Header ────────────────────────────────────────────────
        rx.hstack(
            rx.box(
                rx.icon("message-circle", size=18, color="white"),
                bg=T.PRIMARY,
                border_radius=T.RADIUS_MD,
                padding="0.5rem",
                display="flex", align_items="center", justify_content="center",
            ),
            rx.vstack(
                rx.text("Luyện hội thoại AI",
                        font_size="1.35rem", font_weight="800",
                        color=T.TEXT_PRIMARY, letter_spacing="-0.02em"),
                rx.text(
                    "Trò chuyện với AI để luyện ngoại ngữ theo cặp ngôn ngữ bạn chọn.",
                    font_size="0.85rem", color=T.TEXT_SECONDARY,
                ),
                spacing="0", align="start",
            ),
            spacing="3", align="center", width="100%",
        ),

        # ── Setup panel ───────────────────────────────────────────
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("settings-2", size=16, color=T.PRIMARY),
                    rx.text("Thiết lập phiên học", font_weight="700",
                            font_size="0.95rem", color=T.TEXT_PRIMARY),
                    spacing="2", align="center",
                ),
                rx.grid(
                    rx.vstack(
                        rx.text("Ngôn ngữ bản xứ", font_size="0.78rem",
                                font_weight="600", color=T.TEXT_MUTED,
                                text_transform="uppercase", letter_spacing="0.06em"),
                        rx.select(
                            _LANG_CODES,
                            value=ConversationState.native_lang,
                            on_change=ConversationState.set_native_lang,
                            width="100%",
                            border=f"1.5px solid {T.BORDER}",
                            border_radius=T.RADIUS_MD,
                        ),
                        rx.hstack(
                            rx.text("Cấp độ:", font_size="0.78rem", color=T.TEXT_MUTED),
                            rx.select(
                                _LEVELS,
                                value=ConversationState.native_level,
                                on_change=ConversationState.set_native_level,
                                width="130px",
                                border=f"1px solid {T.BORDER}",
                                border_radius=T.RADIUS_MD,
                            ),
                            spacing="2", align="center",
                        ),
                        spacing="2", align="start",
                    ),
                    rx.box(
                        rx.icon("arrow-right", size=20, color=T.TEXT_MUTED),
                        display="flex", align_items="center", justify_content="center",
                        padding_top="1.5rem",
                    ),
                    rx.vstack(
                        rx.text("Ngôn ngữ đích (luyện)", font_size="0.78rem",
                                font_weight="600", color=T.TEXT_MUTED,
                                text_transform="uppercase", letter_spacing="0.06em"),
                        rx.select(
                            _LANG_CODES,
                            value=ConversationState.foreign_lang,
                            on_change=ConversationState.set_foreign_lang,
                            width="100%",
                            border=f"1.5px solid {T.BORDER}",
                            border_radius=T.RADIUS_MD,
                        ),
                        rx.hstack(
                            rx.text("Cấp độ:", font_size="0.78rem", color=T.TEXT_MUTED),
                            rx.select(
                                _LEVELS,
                                value=ConversationState.foreign_level,
                                on_change=ConversationState.set_foreign_level,
                                width="130px",
                                border=f"1px solid {T.BORDER}",
                                border_radius=T.RADIUS_MD,
                            ),
                            spacing="2", align="center",
                        ),
                        spacing="2", align="start",
                    ),
                    template_columns="1fr 40px 1fr",
                    gap="3",
                    width="100%",
                    align_items="start",
                ),
                rx.button(
                    rx.hstack(
                        rx.cond(
                            ConversationState.loading,
                            rx.icon("loader", size=16),
                            rx.icon("play", size=16),
                        ),
                        rx.text(
                            rx.cond(ConversationState.loading,
                                    "Đang khởi động…", "Bắt đầu phiên học"),
                            font_weight="700",
                        ),
                        spacing="2", align="center",
                    ),
                    on_click=ConversationState.load_lesson,
                    bg=T.PRIMARY,
                    color="white",
                    border_radius=T.RADIUS_PILL,
                    padding="0.7rem 1.5rem",
                    width="100%",
                    _hover={"bg": T.PRIMARY_HOVER},
                ),
                rx.cond(
                    ConversationState.show_error_banner,
                    rx.hstack(
                        rx.icon("alert-circle", size=15, color=T.DANGER),
                        rx.text(ConversationState.error, color=T.DANGER,
                                font_size="0.85rem", font_weight="500"),
                        spacing="2", align="center",
                        padding="0.6rem 0.9rem",
                        border_radius=T.RADIUS_MD,
                        bg=T.DANGER_BG,
                        border=f"1px solid {T.DANGER}",
                        width="100%",
                    ),
                    rx.box(),
                ),
                spacing="4", align="start", width="100%",
            ),
            padding="1.25rem 1.5rem",
            border_radius=T.RADIUS_XL,
            border=f"1px solid {T.BORDER}",
            bg=T.SURFACE,
            box_shadow=T.SHADOW_CARD,
            width="100%",
            max_width="720px",
        ),

        # ── Chat panel ────────────────────────────────────────────
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon("bot", size=14, color=T.PRIMARY),
                        bg=T.PRIMARY_TINT,
                        border_radius="999px",
                        padding="0.3rem",
                        display="flex", align_items="center", justify_content="center",
                    ),
                    rx.text("Tutor AI", font_size="0.85rem", font_weight="700",
                            color=T.PRIMARY),
                    rx.spacer(),
                    rx.cond(
                        ConversationState.loading,
                        rx.hstack(
                            rx.box(
                                width="6px", height="6px",
                                border_radius="999px", bg=T.SUCCESS,
                            ),
                            rx.text("Đang trả lời…", font_size="0.78rem",
                                    color=T.TEXT_MUTED, font_weight="500"),
                            spacing="2", align="center",
                        ),
                        rx.box(),
                    ),
                    width="100%", align="center", spacing="2",
                    padding_bottom="0.75rem",
                    border_bottom=f"1px solid {T.BORDER_LIGHT}",
                ),

                # Messages area
                rx.box(
                    rx.cond(
                        ConversationState.chat_rows.length() == 0,
                        rx.vstack(
                            rx.icon("message-circle", size=40, color=T.BORDER),
                            rx.text("Chọn ngôn ngữ và nhấn «Bắt đầu phiên học»",
                                    font_size="0.9rem", color=T.TEXT_MUTED,
                                    text_align="center"),
                            spacing="3", align="center",
                        ),
                        rx.vstack(
                            rx.foreach(ConversationState.chat_rows, _chat_bubble),
                            spacing="3", width="100%",
                        ),
                    ),
                    min_height="280px",
                    max_height="360px",
                    overflow_y="auto",
                    width="100%",
                    padding="0.5rem 0.25rem",
                ),

                # Input
                rx.hstack(
                    rx.input(
                        placeholder="Nhập câu trả lời của bạn…",
                        value=ConversationState.user_input,
                        on_change=ConversationState.set_user_input,
                        on_key_down=ConversationState.handle_key_press,
                        flex="1",
                        height="44px",
                        border=f"1.5px solid {T.BORDER}",
                        border_radius=T.RADIUS_PILL,
                        padding_x="1.1rem",
                        font_size="0.925rem",
                        bg=T.PAGE_BG,
                        _focus={"border_color": T.PRIMARY,
                                "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                                "bg": T.SURFACE},
                    ),
                    rx.button(
                        rx.icon("send", size=16),
                        on_click=ConversationState.submit_answer,
                        bg=rx.cond(
                            ConversationState.user_input != "",
                            T.PRIMARY, T.PRIMARY_DISABLED,
                        ),
                        color="white",
                        border_radius="999px",
                        width="44px",
                        height="44px",
                        flex_shrink="0",
                        _hover={"bg": T.PRIMARY_HOVER},
                        padding="0",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                    spacing="2", width="100%", align="center",
                ),

                spacing="4", width="100%",
            ),
            padding="1.25rem 1.5rem",
            border_radius=T.RADIUS_XL,
            border=f"1px solid {T.BORDER}",
            bg=T.SURFACE,
            box_shadow=T.SHADOW_CARD,
            width="100%",
            max_width="720px",
        ),

        spacing="4",
        align="start",
        width="100%",
        padding_top="0.5rem",
    )