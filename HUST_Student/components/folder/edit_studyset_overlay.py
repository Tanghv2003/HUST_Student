import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_state import FolderState


# ══════════════════════════════════════════════════════════════════
# WORD ROW — redesigned
# ══════════════════════════════════════════════════════════════════

def _word_row(item: rx.Var):
    return rx.box(
        rx.hstack(
            # ── Index badge ───────────────────────────────────────
            rx.box(
                rx.text(
                    item.idx + 1,
                    font_size="0.72rem",
                    font_weight="800",
                    color=T.PRIMARY,
                    line_height="1",
                ),
                min_width="28px",
                height="28px",
                border_radius="8px",
                bg=T.PRIMARY_TINT,
                border=f"1.5px solid {T.PRIMARY_LIGHT}",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
                margin_top="1.6rem",  # align with inputs
            ),

            # ── Front input ───────────────────────────────────────
            rx.vstack(
                rx.hstack(
                    rx.box(
                        width="6px",
                        height="6px",
                        border_radius="999px",
                        bg=T.PRIMARY,
                        flex_shrink="0",
                    ),
                    rx.text(
                        "Thuật ngữ",
                        font_size="0.7rem",
                        font_weight="700",
                        color=T.TEXT_MUTED,
                        text_transform="uppercase",
                        letter_spacing="0.07em",
                    ),
                    spacing="1",
                    align="center",
                ),
                rx.input(
                    value=item.front,
                    on_change=lambda val: FolderState.update_word_front(item.idx, val),
                    placeholder="Nhập thuật ngữ...",
                    width="100%",
                    height="40px",
                    border=f"1.5px solid {T.BORDER}",
                    border_radius=T.RADIUS_MD,
                    bg=T.PAGE_BG,
                    padding_x="0.85rem",
                    font_size="0.9rem",
                    color=T.TEXT_PRIMARY,
                    _focus={
                        "border_color": T.PRIMARY,
                        "bg": T.SURFACE,
                        "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                        "outline": "none",
                    },
                    _placeholder={"color": T.TEXT_MUTED},
                ),
                spacing="1",
                flex="1",
                align="start",
                min_width="0",
            ),

            # ── Divider arrow ─────────────────────────────────────
            rx.box(
                rx.icon("arrow-right", size=14, color=T.TEXT_MUTED),
                margin_top="1.6rem",
                flex_shrink="0",
                opacity="0.5",
            ),

            # ── Back input ────────────────────────────────────────
            rx.vstack(
                rx.hstack(
                    rx.box(
                        width="6px",
                        height="6px",
                        border_radius="999px",
                        bg=T.SUCCESS,
                        flex_shrink="0",
                    ),
                    rx.text(
                        "Định nghĩa",
                        font_size="0.7rem",
                        font_weight="700",
                        color=T.TEXT_MUTED,
                        text_transform="uppercase",
                        letter_spacing="0.07em",
                    ),
                    spacing="1",
                    align="center",
                ),
                rx.input(
                    value=item.back,
                    on_change=lambda val: FolderState.update_word_back(item.idx, val),
                    placeholder="Nhập định nghĩa...",
                    width="100%",
                    height="40px",
                    border=f"1.5px solid {T.BORDER}",
                    border_radius=T.RADIUS_MD,
                    bg=T.PAGE_BG,
                    padding_x="0.85rem",
                    font_size="0.9rem",
                    color=T.TEXT_PRIMARY,
                    _focus={
                        "border_color": T.SUCCESS,
                        "bg": T.SURFACE,
                        "box_shadow": "0 0 0 3px #d1f5e4",
                        "outline": "none",
                    },
                    _placeholder={"color": T.TEXT_MUTED},
                ),
                spacing="1",
                flex="1",
                align="start",
                min_width="0",
            ),

            # ── Delete button ─────────────────────────────────────
            rx.button(
                rx.icon("trash-2", size=14),
                on_click=FolderState.delete_edit_word(item.idx),
                bg="transparent",
                color=T.BORDER,
                padding="0.4rem",
                border_radius=T.RADIUS_SM,
                border=f"1px solid transparent",
                margin_top="1.6rem",
                flex_shrink="0",
                _hover={
                    "bg": T.DANGER_BG,
                    "color": T.DANGER,
                    "border_color": T.DANGER,
                },
                transition="all 0.15s ease",
            ),

            spacing="3",
            align="start",
            width="100%",
        ),
        width="100%",
        padding="0.85rem 1rem",
        border=f"1px solid {T.BORDER_LIGHT}",
        border_radius=T.RADIUS_MD,
        bg=T.SURFACE,
        transition="border-color 0.15s ease, box-shadow 0.15s ease",
        _hover={
            "border_color": T.BORDER,
            "box_shadow": T.SHADOW_CARD,
        },
    )


# ══════════════════════════════════════════════════════════════════
# TAB BUTTON
# ══════════════════════════════════════════════════════════════════

def _tab_btn(label: str, icon_name: str, mode: str, current_mode):
    is_active = current_mode == mode
    return rx.button(
        rx.hstack(
            rx.icon(icon_name, size=14),
            rx.text(label, font_size="0.82rem", font_weight="600"),
            spacing="1",
            align="center",
        ),
        on_click=lambda: FolderState.set_edit_mode(mode),
        bg=rx.cond(is_active, T.PRIMARY, "transparent"),
        color=rx.cond(is_active, "white", T.TEXT_SECONDARY),
        border=rx.cond(
            is_active,
            f"1.5px solid {T.PRIMARY}",
            f"1.5px solid {T.BORDER}",
        ),
        border_radius=T.RADIUS_MD,
        padding="0.45rem 1rem",
        _hover=rx.cond(
            is_active,
            {"bg": T.PRIMARY_HOVER},
            {"bg": T.BORDER_LIGHT, "color": T.TEXT_PRIMARY},
        ),
        transition="all 0.15s ease",
    )


# ══════════════════════════════════════════════════════════════════
# STATS BAR
# ══════════════════════════════════════════════════════════════════

def _stats_bar():
    return rx.hstack(
        rx.hstack(
            rx.icon("layers", size=13, color=T.PRIMARY),
            rx.text(
                FolderState.edit_words.length(),
                " thẻ",
                font_size="0.78rem",
                font_weight="700",
                color=T.PRIMARY,
            ),
            spacing="1",
            align="center",
            padding="0.3rem 0.65rem",
            bg=T.PRIMARY_TINT,
            border_radius="999px",
            border=f"1px solid {T.PRIMARY_LIGHT}",
        ),
        rx.spacer(),
        rx.text(
            "Cuộn để xem tất cả",
            font_size="0.72rem",
            color=T.TEXT_MUTED,
        ),
        width="100%",
        align="center",
    )


# ══════════════════════════════════════════════════════════════════
# FEEDBACK TOAST
# ══════════════════════════════════════════════════════════════════

def _feedback_toast():
    is_success = FolderState.edit_feedback == "Lưu thành công!"
    return rx.cond(
        FolderState.edit_feedback != "",
        rx.hstack(
            rx.icon(
                rx.cond(is_success, "check-circle", "alert-circle"),
                size=15,
                color=rx.cond(is_success, T.SUCCESS, T.DANGER),
                flex_shrink="0",
            ),
            rx.text(
                FolderState.edit_feedback,
                font_size="0.82rem",
                font_weight="600",
                color=rx.cond(is_success, T.SUCCESS, T.DANGER),
                flex="1",
            ),
            width="100%",
            spacing="2",
            align="center",
            padding="0.6rem 0.85rem",
            bg=rx.cond(is_success, T.SUCCESS_BG, T.DANGER_BG),
            border=rx.cond(
                is_success,
                f"1px solid {T.SUCCESS}",
                f"1px solid {T.DANGER}",
            ),
            border_radius=T.RADIUS_MD,
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# MAIN OVERLAY
# ══════════════════════════════════════════════════════════════════

def edit_studyset_overlay():
    return rx.cond(
        FolderState.show_edit_studyset,
        rx.box(
            rx.box(
                rx.vstack(
                    # ── Header ────────────────────────────────────
                    rx.hstack(
                        rx.hstack(
                            rx.box(
                                rx.icon("pencil", size=16, color="white"),
                                bg=T.PRIMARY,
                                border_radius=T.RADIUS_MD,
                                padding="0.45rem",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                flex_shrink="0",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Chỉnh sửa nội dung bài giảng",
                                    font_size="1.1rem",
                                    font_weight="800",
                                    color=T.TEXT_PRIMARY,
                                    letter_spacing="-0.01em",
                                ),
                                rx.text(
                                    rx.cond(
                                        FolderState.selected_set,
                                        FolderState.selected_set.title,
                                        "",
                                    ),
                                    font_size="0.8rem",
                                    color=T.TEXT_MUTED,
                                    font_weight="500",
                                ),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_edit_studyset),
                        width="100%",
                        align="center",
                    ),

                    rx.divider(border_color=T.BORDER_LIGHT),

                    # ── Tabs ──────────────────────────────────────
                    rx.hstack(
                        _tab_btn("Sửa từng thẻ", "layout-grid", "cards", FolderState.edit_mode),
                        _tab_btn("Sửa cả file (JSON)", "braces", "raw", FolderState.edit_mode),
                        spacing="2",
                        width="100%",
                    ),

                    # ── Feedback ──────────────────────────────────
                    _feedback_toast(),

                    # ── Cards mode ────────────────────────────────
                    rx.cond(
                        FolderState.edit_mode == "cards",
                        rx.vstack(
                            _stats_bar(),
                            rx.box(
                                rx.vstack(
                                    rx.foreach(FolderState.edit_words, _word_row),
                                    spacing="2",
                                    width="100%",
                                    padding_right="0.25rem",
                                ),
                                width="100%",
                                max_height="calc(100dvh - 340px)",
                                overflow_y="auto",
                                # Custom scrollbar styling via css class trick
                                style={
                                    "scrollbar_width": "thin",
                                    "scrollbar_color": f"{T.BORDER} transparent",
                                },
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        # ── Raw JSON mode ─────────────────────────
                        rx.vstack(
                            rx.hstack(
                                rx.icon("info", size=13, color=T.TEXT_MUTED),
                                rx.text(
                                    'Định dạng: [ { "foreign": "...", "native": "..." }, ... ]',
                                    font_size="0.75rem",
                                    color=T.TEXT_MUTED,
                                    font_style="italic",
                                ),
                                spacing="1",
                                align="center",
                            ),
                            rx.text_area(
                                value=FolderState.raw_json_content,
                                on_change=FolderState.set_raw_json_content,
                                placeholder='[ { "foreign": "...", "native": "..." } ]',
                                width="100%",
                                height="360px",
                                border=f"1.5px solid {T.BORDER}",
                                border_radius=T.RADIUS_MD,
                                font_family="'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
                                font_size="0.82rem",
                                line_height="1.6",
                                bg=T.PAGE_BG,
                                padding="0.9rem 1rem",
                                color=T.TEXT_PRIMARY,
                                resize="vertical",
                                _focus={
                                    "border_color": T.PRIMARY,
                                    "bg": T.SURFACE,
                                    "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                                    "outline": "none",
                                },
                            ),
                            spacing="2",
                            width="100%",
                        ),
                    ),

                    # ── Footer ────────────────────────────────────
                    rx.box(
                        height="1px",
                        width="100%",
                        bg=T.BORDER_LIGHT,
                    ),
                    rx.hstack(
                        # Add card button (cards mode only)
                        rx.cond(
                            FolderState.edit_mode == "cards",
                            rx.button(
                                rx.hstack(
                                    rx.icon("plus", size=15),
                                    rx.text("Thêm thẻ", font_size="0.82rem", font_weight="600"),
                                    spacing="1",
                                    align="center",
                                ),
                                on_click=FolderState.add_edit_word,
                                bg=T.PRIMARY_TINT,
                                color=T.PRIMARY,
                                border=f"1.5px solid {T.PRIMARY_LIGHT}",
                                border_radius=T.RADIUS_MD,
                                padding="0.5rem 1rem",
                                _hover={"bg": T.PRIMARY_LIGHT, "border_color": T.PRIMARY},
                                transition="all 0.15s ease",
                            ),
                            rx.box(),
                        ),
                        rx.spacer(),
                        # Cancel
                        rx.button(
                            "Hủy",
                            on_click=FolderState.close_edit_studyset,
                            bg=T.SURFACE,
                            color=T.TEXT_SECONDARY,
                            border=f"1.5px solid {T.BORDER}",
                            border_radius=T.RADIUS_MD,
                            padding="0.5rem 1.1rem",
                            font_weight="600",
                            font_size="0.85rem",
                            _hover={"bg": T.BORDER_LIGHT, "color": T.TEXT_PRIMARY},
                            transition="all 0.15s ease",
                        ),
                        # Save
                        rx.button(
                            rx.hstack(
                                rx.icon("save", size=15),
                                rx.text("Lưu thay đổi", font_size="0.85rem", font_weight="700"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=FolderState.save_edit_studyset,
                            bg=T.SUCCESS,
                            color="white",
                            border=f"1.5px solid {T.SUCCESS}",
                            border_radius=T.RADIUS_MD,
                            padding="0.5rem 1.25rem",
                            _hover={"bg": "#1a9e5c", "border_color": "#1a9e5c"},
                            transition="all 0.15s ease",
                        ),
                        spacing="2",
                        width="100%",
                        align="center",
                    ),

                    spacing="4",
                    padding="1.75rem 2rem",
                    width="100%",
                ),

                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="860px",
                max_width="min(860px, calc(100vw - 2.5rem))",
                max_height=T.MODAL_CONTENT_MAX_HEIGHT,
                min_height="0",
                border=f"1px solid {T.BORDER}",
                box_shadow=T.SHADOW_MODAL,
                overflow="hidden",
                on_click=rx.stop_propagation,
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            display="flex",
            align_items="center",
            justify_content="center",
            bg=T.OVERLAY_SCRIM,
            z_index="999",
            padding=T.MODAL_OVERLAY_PADDING,
            on_click=FolderState.close_edit_studyset,
        ),
        rx.box(),
    )