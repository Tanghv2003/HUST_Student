"""
class_manager_panel.py — UI panel quản lý lớp học.

Chức năng:
  • Thêm / đổi tên / xoá lớp học (đệ quy)
  • Thêm / xoá bài giảng trong lớp
  • Feedback toast tự động (success/error)
  • Đồng bộ sidebar sau mọi thao tác
"""

import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.class_manager_state import ClassManagerState


# ══════════════════════════════════════════════════════════════════
# SHARED COMPONENTS
# ══════════════════════════════════════════════════════════════════

def _action_btn(
    icon: str,
    label: str,
    on_click,
    *,
    danger: bool = False,
    disabled=False,
):
    base_bg = T.DANGER_BG if danger else T.SURFACE
    base_color = T.DANGER if danger else T.TEXT_PRIMARY
    base_border = T.DANGER if danger else T.BORDER
    hover_bg = "#fde0e0" if danger else T.PRIMARY_TINT

    return rx.button(
        rx.hstack(
            rx.icon(icon, size=14),
            rx.text(label, font_size="0.8rem", font_weight="600"),
            spacing="1",
            align="center",
        ),
        on_click=on_click,
        bg=base_bg,
        color=base_color,
        border=f"1px solid {base_border}",
        border_radius=T.RADIUS_MD,
        padding="0.45rem 0.75rem",
        opacity=rx.cond(disabled, "0.45", "1"),
        cursor=rx.cond(disabled, "not-allowed", "pointer"),
        _hover=rx.cond(disabled, {}, {"bg": hover_bg}),
    )


def _simple_modal(
    title: str,
    show,
    close_fn,
    body,
    confirm_label: str,
    confirm_fn,
    *,
    confirm_danger: bool = False,
):
    confirm_bg = T.DANGER if confirm_danger else T.PRIMARY
    confirm_hover = "#c0392b" if confirm_danger else T.PRIMARY_HOVER

    return rx.cond(
        show,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            title,
                            font_size="1.1rem",
                            font_weight="800",
                            color=T.TEXT_PRIMARY,
                        ),
                        rx.spacer(),
                        modal_close_btn(close_fn),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    body,
                    rx.hstack(
                        rx.button(
                            "Hủy",
                            on_click=close_fn,
                            bg=T.BORDER_LIGHT,
                            color=T.TEXT_PRIMARY,
                            border_radius=T.RADIUS_MD,
                            padding="0.5rem 1rem",
                            font_weight="600",
                            _hover={"bg": T.BORDER},
                        ),
                        rx.button(
                            confirm_label,
                            on_click=confirm_fn,
                            bg=confirm_bg,
                            color="white",
                            border_radius=T.RADIUS_MD,
                            padding="0.5rem 1rem",
                            font_weight="700",
                            _hover={"bg": confirm_hover},
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                    ),
                    spacing="4",
                    padding="1.5rem",
                    width="100%",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="460px",
                max_width="min(460px, calc(100vw - 2.5rem))",
                border=f"1px solid {T.BORDER}",
                box_shadow=T.SHADOW_MODAL,
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
            z_index="1000",
            padding="1.75rem 1.25rem",
            on_click=close_fn,
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# MODALS
# ══════════════════════════════════════════════════════════════════

def _add_subclass_modal():
    return _simple_modal(
        "Thêm lớp con",
        ClassManagerState.show_add_subclass_dialog,
        ClassManagerState.close_add_subclass_dialog,
        rx.vstack(
            rx.hstack(
                rx.icon("folder", size=14, color=T.SUCCESS),
                rx.text(
                    ClassManagerState.breadcrumb,
                    font_size="0.8rem",
                    color=T.TEXT_MUTED,
                    no_of_lines=1,
                ),
                spacing="2",
                align="center",
            ),
            rx.vstack(
                rx.text(
                    "Tên lớp con mới *",
                    font_size="0.85rem",
                    font_weight="600",
                    color=T.TEXT_PRIMARY,
                ),
                rx.input(
                    value=ClassManagerState.new_subclass_name,
                    on_change=ClassManagerState.set_new_subclass_name,
                    placeholder="Ví dụ: Nhóm A, Ca sáng...",
                    auto_focus=True,
                    width="100%",
                    border=f"1.5px solid {T.BORDER}",
                    border_radius=T.RADIUS_MD,
                    _focus={
                        "border_color": T.PRIMARY,
                        "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                    },
                ),
                spacing="2",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        "Thêm",
        ClassManagerState.confirm_add_subclass,
    )


def _rename_modal():
    return _simple_modal(
        "Đổi tên lớp",
        ClassManagerState.show_rename_dialog,
        ClassManagerState.close_rename_dialog,
        rx.vstack(
            rx.text(
                "Tên mới",
                font_size="0.85rem",
                font_weight="600",
                color=T.TEXT_PRIMARY,
            ),
            rx.input(
                value=ClassManagerState.new_class_name,
                on_change=ClassManagerState.set_new_class_name,
                placeholder="Nhập tên mới...",
                auto_focus=True,
                width="100%",
                border=f"1.5px solid {T.BORDER}",
                border_radius=T.RADIUS_MD,
                _focus={
                    "border_color": T.PRIMARY,
                    "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                },
            ),
            spacing="2",
            width="100%",
        ),
        "Lưu",
        ClassManagerState.confirm_rename_class,
    )


def _delete_class_modal():
    return _simple_modal(
        "Xoá lớp học",
        ClassManagerState.show_delete_confirmation,
        ClassManagerState.close_delete_confirmation,
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon("alert-triangle", size=20, color=T.DANGER),
                    bg=T.DANGER_BG,
                    border_radius=T.RADIUS_MD,
                    padding="0.5rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
                rx.vstack(
                    rx.text(
                        "Hành động không thể hoàn tác!",
                        font_size="0.9rem",
                        font_weight="700",
                        color=T.DANGER,
                    ),
                    rx.text(
                        "Tất cả lớp con và bài giảng bên trong sẽ bị xoá vĩnh viễn.",
                        font_size="0.85rem",
                        color=T.TEXT_SECONDARY,
                        line_height="1.5",
                    ),
                    spacing="1",
                    align="start",
                ),
                spacing="3",
                align="start",
                width="100%",
            ),
            rx.box(
                rx.hstack(
                    rx.icon("graduation-cap", size=14, color=T.SUCCESS),
                    rx.text(
                        ClassManagerState.breadcrumb,
                        font_size="0.85rem",
                        font_weight="600",
                        color=T.TEXT_PRIMARY,
                        no_of_lines=2,
                    ),
                    spacing="2",
                    align="center",
                ),
                padding="0.75rem 1rem",
                bg=T.BORDER_LIGHT,
                border_radius=T.RADIUS_MD,
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        "Xoá",
        ClassManagerState.confirm_delete_class,
        confirm_danger=True,
    )


def _add_lesson_modal():
    return _simple_modal(
        "Thêm bài giảng",
        ClassManagerState.show_add_lesson_dialog,
        ClassManagerState.close_add_lesson_dialog,
        rx.vstack(
            rx.hstack(
                rx.icon("graduation-cap", size=14, color=T.SUCCESS),
                rx.text(
                    ClassManagerState.breadcrumb,
                    font_size="0.8rem",
                    color=T.TEXT_MUTED,
                    no_of_lines=1,
                ),
                spacing="2",
                align="center",
            ),
            rx.vstack(
                rx.text(
                    "Tên bài giảng *",
                    font_size="0.85rem",
                    font_weight="600",
                    color=T.TEXT_PRIMARY,
                ),
                rx.input(
                    value=ClassManagerState.new_lesson_title,
                    on_change=ClassManagerState.set_new_lesson_title,
                    placeholder="Ví dụ: Buổi học số 1",
                    auto_focus=True,
                    width="100%",
                    border=f"1.5px solid {T.BORDER}",
                    border_radius=T.RADIUS_MD,
                    _focus={
                        "border_color": T.PRIMARY,
                        "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                    },
                ),
                spacing="1",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Đường dẫn file JSON *",
                    font_size="0.85rem",
                    font_weight="600",
                    color=T.TEXT_PRIMARY,
                ),
                rx.input(
                    value=ClassManagerState.new_lesson_file,
                    on_change=ClassManagerState.set_new_lesson_file,
                    placeholder="Ví dụ: nihongo/a.json",
                    width="100%",
                    border=f"1.5px solid {T.BORDER}",
                    border_radius=T.RADIUS_MD,
                    _focus={
                        "border_color": T.PRIMARY,
                        "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}",
                    },
                ),
                rx.text(
                    "Đường dẫn tương đối trong thư mục data/class/",
                    font_size="0.75rem",
                    color=T.TEXT_MUTED,
                ),
                spacing="1",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        "Thêm",
        ClassManagerState.confirm_add_lesson,
    )


# ══════════════════════════════════════════════════════════════════
# TREE ROW
# ══════════════════════════════════════════════════════════════════

def _tree_row(row: dict):
    is_selected = ClassManagerState.selected_path_key == row["path_key"]

    return rx.box(
        rx.hstack(
            rx.box(width=row["indent_px"], flex_shrink="0"),
            rx.icon("graduation-cap", size=15, color=T.SUCCESS, flex_shrink="0"),
            rx.vstack(
                rx.text(
                    row["name"],
                    font_size="0.875rem",
                    font_weight=rx.cond(is_selected, "700", "500"),
                    color=rx.cond(is_selected, T.PRIMARY, T.TEXT_PRIMARY),
                    no_of_lines=1,
                ),
                rx.cond(
                    row["subtitle"] != "",
                    rx.text(
                        row["subtitle"],
                        font_size="0.68rem",
                        color=T.TEXT_MUTED,
                        no_of_lines=1,
                    ),
                    rx.box(),
                ),
                spacing="0",
                align="start",
                flex="1",
                min_width="0",
            ),
            rx.cond(
                is_selected,
                rx.icon("check", size=14, color=T.PRIMARY, flex_shrink="0"),
                rx.box(width="14px", flex_shrink="0"),
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        width="100%",
        padding="0.5rem 0.65rem",
        bg=rx.cond(is_selected, T.PRIMARY_TINT, T.SURFACE),
        border=rx.cond(
            is_selected,
            f"1.5px solid {T.PRIMARY}",
            f"1px solid {T.BORDER}",
        ),
        border_radius=T.RADIUS_MD,
        cursor="pointer",
        transition="all 0.1s ease",
        on_click=ClassManagerState.select_class(row["path_key"]),
        _hover=rx.cond(
            is_selected, {}, {"bg": T.PRIMARY_TINT, "border_color": T.PRIMARY}
        ),
    )


# ══════════════════════════════════════════════════════════════════
# LESSON ROW
# ══════════════════════════════════════════════════════════════════

def _lesson_row_item(item: dict):
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("book-open", size=14, color=T.PRIMARY),
                bg=T.PRIMARY_TINT,
                border_radius=T.RADIUS_SM,
                padding="0.3rem",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(
                    item["title"],
                    font_size="0.875rem",
                    font_weight="600",
                    color=T.TEXT_PRIMARY,
                    no_of_lines=1,
                ),
                rx.hstack(
                    rx.text(
                        item["file"],
                        font_size="0.68rem",
                        color=T.TEXT_MUTED,
                        no_of_lines=1,
                        flex="1",
                    ),
                    rx.text(
                        item["terms_label"],
                        font_size="0.68rem",
                        color=T.TEXT_MUTED,
                        white_space="nowrap",
                        flex_shrink="0",
                    ),
                    width="100%",
                    spacing="2",
                    align="center",
                ),
                spacing="0",
                align="start",
                flex="1",
                min_width="0",
            ),
            rx.button(
                rx.icon("trash-2", size=13),
                on_click=ClassManagerState.remove_lesson_item(item["title"]),
                bg="transparent",
                color=T.TEXT_MUTED,
                padding="0.3rem",
                border_radius=T.RADIUS_SM,
                _hover={"bg": T.DANGER_BG, "color": T.DANGER},
                title="Xoá bài giảng",
                flex_shrink="0",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        width="100%",
        padding="0.65rem 0.9rem",
        bg=T.SURFACE,
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_MD,
        transition="border-color 0.1s ease",
        _hover={"border_color": T.PRIMARY},
    )


# ══════════════════════════════════════════════════════════════════
# MESSAGE TOAST
# ══════════════════════════════════════════════════════════════════

def _message_toast():
    return rx.cond(
        ClassManagerState.message != "",
        rx.box(
            rx.hstack(
                rx.icon(
                    rx.cond(
                        ClassManagerState.message_type == "error",
                        "alert-circle",
                        "check-circle",
                    ),
                    size=16,
                    color=rx.cond(
                        ClassManagerState.message_type == "error",
                        T.DANGER,
                        T.SUCCESS,
                    ),
                    flex_shrink="0",
                ),
                rx.text(
                    ClassManagerState.message,
                    font_size="0.85rem",
                    font_weight="500",
                    flex="1",
                    color=rx.cond(
                        ClassManagerState.message_type == "error",
                        T.DANGER,
                        T.SUCCESS,
                    ),
                ),
                rx.button(
                    rx.icon("x", size=14),
                    on_click=ClassManagerState.clear_message,
                    bg="transparent",
                    padding="0.2rem",
                    color=T.TEXT_MUTED,
                    _hover={"color": T.TEXT_PRIMARY},
                    flex_shrink="0",
                ),
                width="100%",
                spacing="2",
                align="center",
            ),
            width="100%",
            padding="0.65rem 0.9rem",
            border_radius=T.RADIUS_MD,
            bg=rx.cond(
                ClassManagerState.message_type == "error",
                T.DANGER_BG,
                T.SUCCESS_BG,
            ),
            border=rx.cond(
                ClassManagerState.message_type == "error",
                f"1px solid {T.DANGER}",
                f"1px solid {T.SUCCESS}",
            ),
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# MAIN PANEL
# ══════════════════════════════════════════════════════════════════

def class_manager_panel():
    return rx.box(
        # ── All modals ──────────────────────────────────────────
        _add_subclass_modal(),
        _rename_modal(),
        _delete_class_modal(),
        _add_lesson_modal(),

        rx.vstack(
            # ── Header ─────────────────────────────────────────
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "Quản lý lớp học",
                        font_size="1rem",
                        font_weight="700",
                        color=T.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Thêm, đổi tên hoặc xoá lớp và bài giảng",
                        font_size="0.78rem",
                        color=T.TEXT_MUTED,
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("home", size=13),
                        rx.text("Gốc", font_size="0.8rem", font_weight="600"),
                        spacing="1",
                        align="center",
                    ),
                    on_click=ClassManagerState.select_class(""),
                    bg=rx.cond(
                        ClassManagerState.is_at_root, T.PRIMARY, T.BORDER_LIGHT
                    ),
                    color=rx.cond(
                        ClassManagerState.is_at_root, "white", T.TEXT_PRIMARY
                    ),
                    border_radius=T.RADIUS_MD,
                    padding="0.4rem 0.85rem",
                    _hover=rx.cond(
                        ClassManagerState.is_at_root,
                        {},
                        {"bg": T.PRIMARY_TINT, "color": T.PRIMARY},
                    ),
                ),
                width="100%",
                align="center",
            ),

            # ── Breadcrumb + summary ────────────────────────────
            rx.box(
                rx.hstack(
                    rx.cond(
                        ClassManagerState.is_at_root,
                        rx.icon("layers", size=16, color=T.PRIMARY),
                        rx.icon("graduation-cap", size=16, color=T.SUCCESS),
                    ),
                    rx.vstack(
                        rx.text(
                            ClassManagerState.breadcrumb,
                            font_size="0.9rem",
                            font_weight="700",
                            color=T.TEXT_PRIMARY,
                            no_of_lines=2,
                        ),
                        rx.text(
                            ClassManagerState.class_summary,
                            font_size="0.75rem",
                            color=T.TEXT_SECONDARY,
                        ),
                        spacing="0",
                        align="start",
                        flex="1",
                    ),
                    spacing="2",
                    align="start",
                    width="100%",
                ),
                width="100%",
                padding="0.7rem 0.9rem",
                bg=T.BORDER_LIGHT,
                border_radius=T.RADIUS_MD,
                border=f"1px solid {T.BORDER}",
            ),

            # ── Message toast ───────────────────────────────────
            _message_toast(),

            # ── Action buttons ──────────────────────────────────
            rx.grid(
                _action_btn(
                    "folder-plus",
                    "Thêm lớp con",
                    ClassManagerState.open_add_subclass_dialog,
                ),
                _action_btn(
                    "pencil",
                    "Đổi tên lớp",
                    ClassManagerState.open_rename_dialog,
                    disabled=ClassManagerState.is_at_root,
                ),
                _action_btn(
                    "book-plus",
                    "Thêm bài giảng",
                    ClassManagerState.open_add_lesson_dialog,
                    disabled=ClassManagerState.is_at_root,
                ),
                _action_btn(
                    "trash-2",
                    "Xoá lớp",
                    ClassManagerState.open_delete_confirmation,
                    danger=True,
                    disabled=ClassManagerState.is_at_root,
                ),
                grid_template_columns="repeat(2, 1fr)",
                gap="2",
                width="100%",
            ),

            # ── Lessons in selected class ───────────────────────
            rx.cond(
                ~ClassManagerState.is_at_root,
                rx.vstack(
                    rx.hstack(
                        rx.icon("book-open", size=15, color=T.PRIMARY),
                        rx.text(
                            "Bài giảng trong lớp này",
                            font_size="0.85rem",
                            font_weight="700",
                            color=T.TEXT_PRIMARY,
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.cond(
                        ClassManagerState.class_lessons.length() > 0,
                        rx.vstack(
                            rx.foreach(
                                ClassManagerState.class_lessons, _lesson_row_item
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.icon("book-open", size=24, color=T.BORDER),
                                rx.text(
                                    "Chưa có bài giảng nào.",
                                    font_size="0.82rem",
                                    color=T.TEXT_MUTED,
                                    text_align="center",
                                ),
                                rx.text(
                                    "Nhấn «Thêm bài giảng» để thêm file JSON.",
                                    font_size="0.78rem",
                                    color=T.TEXT_MUTED,
                                    text_align="center",
                                ),
                                spacing="1",
                                align="center",
                            ),
                            padding="1.5rem",
                            width="100%",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            bg=T.BORDER_LIGHT,
                            border_radius=T.RADIUS_MD,
                            border=f"1px dashed {T.BORDER}",
                        ),
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.box(),
            ),

            # ── Full class tree ─────────────────────────────────
            rx.vstack(
                rx.hstack(
                    rx.icon("graduation-cap", size=15, color=T.SUCCESS),
                    rx.text(
                        "Toàn bộ lớp học",
                        font_size="0.85rem",
                        font_weight="700",
                        color=T.TEXT_PRIMARY,
                    ),
                    rx.spacer(),
                    rx.text(
                        ClassManagerState.tree_rows.length(),
                        font_size="0.75rem",
                        color=T.TEXT_MUTED,
                        font_weight="600",
                    ),
                    spacing="2",
                    align="center",
                    width="100%",
                ),
                rx.box(
                    rx.cond(
                        ClassManagerState.tree_rows.length() > 0,
                        rx.vstack(
                            rx.foreach(ClassManagerState.tree_rows, _tree_row),
                            spacing="1",
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.icon("folder-plus", size=28, color=T.BORDER),
                                rx.text(
                                    "Chưa có lớp học nào.",
                                    font_size="0.85rem",
                                    color=T.TEXT_MUTED,
                                    text_align="center",
                                ),
                                rx.text(
                                    "Nhấn «Thêm lớp con» để tạo lớp đầu tiên.",
                                    font_size="0.78rem",
                                    color=T.TEXT_MUTED,
                                    text_align="center",
                                ),
                                spacing="2",
                                align="center",
                            ),
                            padding="2rem",
                            width="100%",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                    ),
                    width="100%",
                    max_height="380px",
                    overflow_y="auto",
                    border=f"1px solid {T.BORDER}",
                    border_radius=T.RADIUS_LG,
                    padding="0.5rem",
                    bg=T.SURFACE,
                ),
                spacing="2",
                width="100%",
            ),

            spacing="3",
            width="100%",
            align="start",
        ),
        width="100%",
        on_mount=ClassManagerState.load_current_class,
    )