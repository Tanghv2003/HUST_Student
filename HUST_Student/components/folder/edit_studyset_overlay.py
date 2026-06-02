import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_state import FolderState


def _word_row(item: rx.Var):
    return rx.box(
        rx.hstack(
            # Index indicator
            rx.center(
                rx.text(
                    item.idx + 1,
                    font_size="0.9rem",
                    font_weight="700",
                    color=T.PRIMARY,
                ),
                bg=T.PRIMARY_LIGHT,
                width="32px",
                height="32px",
                border_radius="50%",
                flex_shrink="0",
            ),
            # Front side input
            rx.vstack(
                rx.text("Thuật ngữ (Mặt trước)", font_size="0.75rem", font_weight="600", color=T.TEXT_SECONDARY),
                rx.input(
                    value=item.front,
                    on_change=lambda val: FolderState.update_word_front(item.idx, val),
                    placeholder="Nhập thuật ngữ...",
                    width="100%",
                    border=f"1px solid {T.BORDER}",
                    border_radius=T.RADIUS_SM,
                    bg=T.PAGE_BG,
                    padding="0.5rem 0.75rem",
                    _focus={"border_color": T.PRIMARY, "bg": T.SURFACE},
                ),
                spacing="1",
                flex="1",
                align="start",
            ),
            # Back side input
            rx.vstack(
                rx.text("Định nghĩa (Mặt sau)", font_size="0.75rem", font_weight="600", color=T.TEXT_SECONDARY),
                rx.input(
                    value=item.back,
                    on_change=lambda val: FolderState.update_word_back(item.idx, val),
                    placeholder="Nhập định nghĩa...",
                    width="100%",
                    border=f"1px solid {T.BORDER}",
                    border_radius=T.RADIUS_SM,
                    bg=T.PAGE_BG,
                    padding="0.5rem 0.75rem",
                    _focus={"border_color": T.PRIMARY, "bg": T.SURFACE},
                ),
                spacing="1",
                flex="1",
                align="start",
            ),
            # Delete button
            rx.button(
                rx.icon("trash-2", size=16),
                on_click=FolderState.delete_edit_word(item.idx),
                bg="transparent",
                color=T.TEXT_MUTED,
                padding="0.5rem",
                border_radius=T.RADIUS_SM,
                _hover={"bg": T.DANGER_BG, "color": T.DANGER},
                margin_top="1.25rem",  # Align with inputs
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        width="100%",
        padding="1rem",
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_MD,
        bg=T.SURFACE,
        box_shadow=T.SHADOW_CARD,
    )


def edit_studyset_overlay():
    return rx.cond(
        FolderState.show_edit_studyset,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.hstack(
                            rx.icon("pencil", size=20, color=T.PRIMARY),
                            rx.vstack(
                                rx.text(
                                    "Chỉnh sửa nội dung bài giảng",
                                    font_size="1.25rem",
                                    font_weight="800",
                                    color=T.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    rx.cond(
                                        FolderState.selected_set,
                                        FolderState.selected_set.title,
                                        "",
                                    ),
                                    font_size="0.85rem",
                                    color=T.TEXT_SECONDARY,
                                    font_weight="600",
                                ),
                                spacing="0",
                                align="start",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_edit_studyset),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),

                    # Tabs to toggle editor modes
                    rx.hstack(
                        rx.button(
                            rx.hstack(
                                rx.icon("layout-grid", size=14),
                                rx.text("Sửa từng thẻ", font_size="0.85rem"),
                                spacing="1",
                                align="center",
                            ),
                            on_click=lambda: FolderState.set_edit_mode("cards"),
                            bg=rx.cond(FolderState.edit_mode == "cards", T.PRIMARY, "transparent"),
                            color=rx.cond(FolderState.edit_mode == "cards", "white", T.TEXT_SECONDARY),
                            border=f"1px solid {T.BORDER}",
                            border_radius=T.RADIUS_MD,
                            padding="0.45rem 1rem",
                            font_weight="600",
                            _hover={"bg": rx.cond(FolderState.edit_mode == "cards", T.PRIMARY_HOVER, T.BORDER_LIGHT)},
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon("braces", size=14),
                                rx.text("Sửa cả file (JSON)", font_size="0.85rem"),
                                spacing="1",
                                align="center",
                            ),
                            on_click=lambda: FolderState.set_edit_mode("raw"),
                            bg=rx.cond(FolderState.edit_mode == "raw", T.PRIMARY, "transparent"),
                            color=rx.cond(FolderState.edit_mode == "raw", "white", T.TEXT_SECONDARY),
                            border=f"1px solid {T.BORDER}",
                            border_radius=T.RADIUS_MD,
                            padding="0.45rem 1rem",
                            font_weight="600",
                            _hover={"bg": rx.cond(FolderState.edit_mode == "raw", T.PRIMARY_HOVER, T.BORDER_LIGHT)},
                        ),
                        spacing="2",
                        width="100%",
                        border_bottom=f"1px solid {T.DIVIDER}",
                        padding_bottom="0.75rem",
                    ),

                    # Feedback toast/message
                    rx.cond(
                        FolderState.edit_feedback != "",
                        rx.box(
                            rx.text(
                                FolderState.edit_feedback,
                                font_size="0.85rem",
                                font_weight="600",
                                color=T.DANGER,
                            ),
                            width="100%",
                            padding="0.5rem 1rem",
                            bg=T.DANGER_BG,
                            border=f"1px solid {T.DANGER}",
                            border_radius=T.RADIUS_SM,
                        ),
                        rx.box(),
                    ),

                    # Editor body based on edit_mode
                    rx.cond(
                        FolderState.edit_mode == "cards",
                        # Scrollable list of terms (cards)
                        rx.box(
                            rx.vstack(
                                rx.foreach(
                                    FolderState.edit_words,
                                    _word_row,
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            width="100%",
                            max_height="calc(100vh - 280px)",
                            overflow_y="auto",
                            padding_right="0.5rem",
                        ),
                        # Raw JSON text editor
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Định dạng JSON: Danh sách các đối tượng dạng [ { \"foreign\": \"...\", \"native\": \"...\" }, ... ]",
                                    font_size="0.78rem",
                                    color=T.TEXT_MUTED,
                                    font_style="italic",
                                ),
                                rx.text_area(
                                    value=FolderState.raw_json_content,
                                    on_change=FolderState.set_raw_json_content,
                                    placeholder="[ { \"foreign\": \"...\", \"native\": \"...\" } ]",
                                    width="100%",
                                    height="360px",
                                    border=f"1px solid {T.BORDER}",
                                    border_radius=T.RADIUS_MD,
                                    font_family="monospace",
                                    font_size="0.85rem",
                                    line_height="1.5",
                                    bg=T.PAGE_BG,
                                    padding="1rem",
                                    _focus={"border_color": T.PRIMARY, "bg": T.SURFACE},
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            width="100%",
                        ),
                    ),

                    # Footer/Action buttons
                    rx.hstack(
                        # Add new card button (only in cards mode)
                        rx.cond(
                            FolderState.edit_mode == "cards",
                            rx.button(
                                rx.hstack(
                                    rx.icon("plus", size=16),
                                    rx.text("Thêm thẻ mới", font_size="0.85rem"),
                                    spacing="1",
                                    align="center",
                                ),
                                on_click=FolderState.add_edit_word,
                                bg=T.PRIMARY_LIGHT,
                                color=T.PRIMARY,
                                border_radius=T.RADIUS_MD,
                                padding="0.6rem 1rem",
                                font_weight="700",
                                _hover={"bg": T.PRIMARY_TINT},
                            ),
                            rx.box(),
                        ),
                        rx.spacer(),
                        # Cancel button
                        rx.button(
                            "Hủy",
                            on_click=FolderState.close_edit_studyset,
                            bg=T.BORDER_LIGHT,
                            color=T.TEXT_PRIMARY,
                            border_radius=T.RADIUS_MD,
                            padding="0.6rem 1.2rem",
                            font_weight="600",
                            _hover={"bg": T.BORDER},
                        ),
                        # Save button
                        rx.button(
                            rx.hstack(
                                rx.icon("save", size=16),
                                rx.text("Lưu thay đổi", font_size="0.85rem"),
                                spacing="1",
                                align="center",
                            ),
                            on_click=FolderState.save_edit_studyset,
                            bg=T.SUCCESS,
                            color="white",
                            border_radius=T.RADIUS_MD,
                            padding="0.6rem 1.2rem",
                            font_weight="700",
                            _hover={"bg": "#1c8f56"},
                        ),
                        spacing="3",
                        width="100%",
                        align="center",
                    ),
                    spacing="5",
                    width="100%",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="840px",
                max_width="min(840px, calc(100vw - 2.5rem))",
                max_height=T.MODAL_CONTENT_MAX_HEIGHT,
                min_height="0",
                border=f"1px solid {T.BORDER}",
                box_shadow=T.SHADOW_MODAL,
                padding="2.25rem",
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
