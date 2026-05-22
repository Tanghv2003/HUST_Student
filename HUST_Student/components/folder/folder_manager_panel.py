"""
folder_manager_panel.py — UI panel quản lý thư mục & bài giảng.

Chức năng:
  • Cây thư mục dạng flat với indent
  • Thêm / đổi tên / xoá folder con
  • Thêm / đổi tên / xoá bài giảng
  • Feedback toast tự động (success/error)
  • Đồng bộ sidebar sau mọi thao tác
"""

import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_manager_state import FolderManagerState


# ══════════════════════════════════════════════════════════════════
# SHARED COMPONENTS
# ══════════════════════════════════════════════════════════════════

def _action_btn(icon: str, label: str, on_click, *, danger: bool = False, disabled: bool = False):
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
        _hover=rx.cond(disabled, {}, {"bg": hover_bg, "border_color": base_border}),
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
                        rx.text(title, font_size="1.1rem", font_weight="800", color=T.TEXT_PRIMARY),
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
            top="0", left="0", right="0", bottom="0",
            display="flex",
            align_items="center",
            justify_content="center",
            bg=T.OVERLAY_SCRIM,
            z_index="1000",
            padding=T.MODAL_OVERLAY_PADDING,
            on_click=close_fn,
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# MODALS
# ══════════════════════════════════════════════════════════════════

def _add_subfolder_modal():
    return _simple_modal(
        "Thêm thư mục con",
        FolderManagerState.show_add_subfolder_dialog,
        FolderManagerState.close_add_subfolder_dialog,
        rx.vstack(
            rx.hstack(
                rx.icon("folder", size=14, color=T.WARN),
                rx.text(
                    FolderManagerState.breadcrumb,
                    font_size="0.8rem",
                    color=T.TEXT_MUTED,
                    no_of_lines=1,
                ),
                spacing="2",
                align="center",
            ),
            rx.vstack(
                rx.text("Tên thư mục mới", font_size="0.85rem", font_weight="600", color=T.TEXT_PRIMARY),
                rx.input(
                    value=FolderManagerState.new_subfolder_name,
                    on_change=FolderManagerState.set_new_subfolder_name,
                    placeholder="Nhập tên thư mục...",
                    auto_focus=True,
                    width="100%",
                    border=f"1.5px solid {T.BORDER}",
                    border_radius=T.RADIUS_MD,
                    _focus={"border_color": T.PRIMARY, "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}"},
                ),
                spacing="2",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        "Thêm",
        FolderManagerState.confirm_add_subfolder,
    )


def _rename_modal():
    return _simple_modal(
        "Đổi tên thư mục",
        FolderManagerState.show_rename_dialog,
        FolderManagerState.close_rename_dialog,
        rx.vstack(
            rx.text("Tên mới", font_size="0.85rem", font_weight="600", color=T.TEXT_PRIMARY),
            rx.input(
                value=FolderManagerState.new_folder_name,
                on_change=FolderManagerState.set_new_folder_name,
                placeholder="Nhập tên mới...",
                auto_focus=True,
                width="100%",
                border=f"1.5px solid {T.BORDER}",
                border_radius=T.RADIUS_MD,
                _focus={"border_color": T.PRIMARY, "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}"},
            ),
            spacing="2",
            width="100%",
        ),
        "Lưu",
        FolderManagerState.confirm_rename_folder,
    )


def _delete_folder_modal():
    return _simple_modal(
        "Xoá thư mục",
        FolderManagerState.show_delete_confirmation,
        FolderManagerState.close_delete_confirmation,
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
                        "Tất cả thư mục con và bài giảng bên trong sẽ bị xoá vĩnh viễn.",
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
                    rx.icon("folder", size=14, color=T.WARN),
                    rx.text(
                        FolderManagerState.breadcrumb,
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
        FolderManagerState.confirm_delete_folder,
        confirm_danger=True,
    )


def _add_studyset_modal():
    return _simple_modal(
        "Thêm bài giảng",
        FolderManagerState.show_add_studyset_dialog,
        FolderManagerState.close_add_studyset_dialog,
        rx.vstack(
            rx.hstack(
                rx.icon("folder", size=14, color=T.WARN),
                rx.text(
                    FolderManagerState.breadcrumb,
                    font_size="0.8rem",
                    color=T.TEXT_MUTED,
                    no_of_lines=1,
                ),
                spacing="2",
                align="center",
            ),
            rx.vstack(
                rx.text("Tên bài giảng *", font_size="0.85rem", font_weight="600", color=T.TEXT_PRIMARY),
                rx.input(
                    value=FolderManagerState.new_studyset_title,
                    on_change=FolderManagerState.set_new_studyset_title,
                    placeholder="Ví dụ: Từ vựng Bài 21",
                    auto_focus=True,
                    width="100%",
                    border=f"1.5px solid {T.BORDER}",
                    border_radius=T.RADIUS_MD,
                    _focus={"border_color": T.PRIMARY, "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}"},
                ),
                spacing="1",
                width="100%",
            ),
            rx.vstack(
                rx.text("Đường dẫn file JSON *", font_size="0.85rem", font_weight="600", color=T.TEXT_PRIMARY),
                rx.input(
                    value=FolderManagerState.new_studyset_file,
                    on_change=FolderManagerState.set_new_studyset_file,
                    placeholder="Ví dụ: nihongo/daichi/Bai_21-Tu_vung.json",
                    width="100%",
                    border=f"1.5px solid {T.BORDER}",
                    border_radius=T.RADIUS_MD,
                    _focus={"border_color": T.PRIMARY, "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}"},
                ),
                rx.text(
                    "Đường dẫn tương đối trong thư mục data/studysets/",
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
        FolderManagerState.confirm_add_studyset,
    )


def _rename_studyset_modal():
    return _simple_modal(
        "Đổi tên bài giảng",
        FolderManagerState.show_rename_studyset_dialog,
        FolderManagerState.close_rename_studyset_dialog,
        rx.vstack(
            rx.text("Tên mới", font_size="0.85rem", font_weight="600", color=T.TEXT_PRIMARY),
            rx.input(
                value=FolderManagerState.rename_studyset_new_title,
                on_change=FolderManagerState.set_rename_studyset_new_title,
                placeholder="Nhập tên mới...",
                auto_focus=True,
                width="100%",
                border=f"1.5px solid {T.BORDER}",
                border_radius=T.RADIUS_MD,
                _focus={"border_color": T.PRIMARY, "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}"},
            ),
            spacing="2",
            width="100%",
        ),
        "Lưu",
        FolderManagerState.confirm_rename_studyset,
    )


def _delete_studyset_modal():
    return _simple_modal(
        "Xoá bài giảng",
        FolderManagerState.show_delete_studyset_confirmation,
        FolderManagerState.close_delete_studyset_confirmation,
        rx.text(
            rx.fragment("Xoá bài giảng "),
            rx.text(
                FolderManagerState.delete_studyset_title,
                as_="span",
                font_weight="700",
                color=T.TEXT_PRIMARY,
            ),
            rx.fragment("? Hành động này không thể hoàn tác."),
            font_size="0.9rem",
            color=T.TEXT_SECONDARY,
            line_height="1.6",
        ),
        "Xoá",
        FolderManagerState.confirm_delete_studyset,
        confirm_danger=True,
    )


# ══════════════════════════════════════════════════════════════════
# TREE ROW
# ══════════════════════════════════════════════════════════════════

def _tree_row(row: dict):
    is_selected = FolderManagerState.selected_path_key == row["path_key"]

    return rx.box(
        rx.hstack(
            rx.box(width=row["indent_px"], flex_shrink="0"),
            rx.cond(
                row["has_children"],
                rx.icon("folder", size=15, color=T.WARN, flex_shrink="0"),
                rx.icon("folder-open", size=15, color=T.WARN, flex_shrink="0"),
            ),
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
        on_click=FolderManagerState.select_folder(row["path_key"]),
        _hover=rx.cond(is_selected, {}, {"bg": T.PRIMARY_TINT, "border_color": T.PRIMARY}),
    )


# ══════════════════════════════════════════════════════════════════
# STUDYSET ROW
# ══════════════════════════════════════════════════════════════════

def _studyset_row(item: dict):
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
            # Action buttons
            rx.hstack(
                rx.button(
                    rx.icon("pencil", size=13),
                    on_click=FolderManagerState.open_rename_studyset_dialog(item["title"]),
                    bg="transparent",
                    color=T.TEXT_MUTED,
                    padding="0.3rem",
                    border_radius=T.RADIUS_SM,
                    _hover={"bg": T.PRIMARY_TINT, "color": T.PRIMARY},
                    title="Đổi tên",
                ),
                rx.button(
                    rx.icon("trash-2", size=13),
                    on_click=FolderManagerState.open_delete_studyset_confirmation(item["title"]),
                    bg="transparent",
                    color=T.TEXT_MUTED,
                    padding="0.3rem",
                    border_radius=T.RADIUS_SM,
                    _hover={"bg": T.DANGER_BG, "color": T.DANGER},
                    title="Xoá",
                ),
                spacing="0",
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
        FolderManagerState.message != "",
        rx.box(
            rx.hstack(
                rx.icon(
                    rx.cond(
                        FolderManagerState.message_type == "error",
                        "alert-circle",
                        "check-circle",
                    ),
                    size=16,
                    color=rx.cond(
                        FolderManagerState.message_type == "error",
                        T.DANGER,
                        T.SUCCESS,
                    ),
                    flex_shrink="0",
                ),
                rx.text(
                    FolderManagerState.message,
                    font_size="0.85rem",
                    font_weight="500",
                    flex="1",
                    color=rx.cond(
                        FolderManagerState.message_type == "error",
                        T.DANGER,
                        T.SUCCESS,
                    ),
                ),
                rx.button(
                    rx.icon("x", size=14),
                    on_click=FolderManagerState.clear_message,
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
                FolderManagerState.message_type == "error",
                T.DANGER_BG,
                T.SUCCESS_BG,
            ),
            border=rx.cond(
                FolderManagerState.message_type == "error",
                f"1px solid {T.DANGER}",
                f"1px solid {T.SUCCESS}",
            ),
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# MAIN PANEL
# ══════════════════════════════════════════════════════════════════

def folder_manager_panel():
    return rx.box(
        # ── All modals ──────────────────────────────────────────
        _add_subfolder_modal(),
        _rename_modal(),
        _delete_folder_modal(),
        _add_studyset_modal(),
        _rename_studyset_modal(),
        _delete_studyset_modal(),

        rx.vstack(
            # ── Header ─────────────────────────────────────────
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "Quản lý thư mục",
                        font_size="1rem",
                        font_weight="700",
                        color=T.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Thêm, đổi tên hoặc xoá thư mục và bài giảng",
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
                    on_click=FolderManagerState.select_folder(""),
                    bg=rx.cond(FolderManagerState.is_at_root, T.PRIMARY, T.BORDER_LIGHT),
                    color=rx.cond(FolderManagerState.is_at_root, "white", T.TEXT_PRIMARY),
                    border_radius=T.RADIUS_MD,
                    padding="0.4rem 0.85rem",
                    _hover=rx.cond(
                        FolderManagerState.is_at_root,
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
                        FolderManagerState.is_at_root,
                        rx.icon("layers", size=16, color=T.PRIMARY),
                        rx.icon("folder-open", size=16, color=T.WARN),
                    ),
                    rx.vstack(
                        rx.text(
                            FolderManagerState.breadcrumb,
                            font_size="0.9rem",
                            font_weight="700",
                            color=T.TEXT_PRIMARY,
                            no_of_lines=2,
                        ),
                        rx.text(
                            FolderManagerState.folder_summary,
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
                    "Thêm thư mục con",
                    FolderManagerState.open_add_subfolder_dialog,
                ),
                _action_btn(
                    "pencil",
                    "Đổi tên thư mục",
                    FolderManagerState.open_rename_dialog,
                    disabled=FolderManagerState.is_at_root,
                ),
                _action_btn(
                    "book-plus",
                    "Thêm bài giảng",
                    FolderManagerState.open_add_studyset_dialog,
                    disabled=FolderManagerState.is_at_root,
                ),
                _action_btn(
                    "trash-2",
                    "Xoá thư mục",
                    FolderManagerState.open_delete_confirmation,
                    danger=True,
                    disabled=FolderManagerState.is_at_root,
                ),
                grid_template_columns="repeat(2, 1fr)",
                gap="2",
                width="100%",
            ),

            # ── Studysets in selected folder ────────────────────
            rx.cond(
                ~FolderManagerState.is_at_root,
                rx.vstack(
                    rx.hstack(
                        rx.icon("book-open", size=15, color=T.PRIMARY),
                        rx.text(
                            "Bài giảng trong thư mục này",
                            font_size="0.85rem",
                            font_weight="700",
                            color=T.TEXT_PRIMARY,
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.cond(
                        FolderManagerState.folder_studysets.length() > 0,
                        rx.vstack(
                            rx.foreach(FolderManagerState.folder_studysets, _studyset_row),
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

            # ── Folder tree ─────────────────────────────────────
            rx.vstack(
                rx.hstack(
                    rx.icon("folder", size=15, color=T.WARN),
                    rx.text(
                        "Toàn bộ thư mục",
                        font_size="0.85rem",
                        font_weight="700",
                        color=T.TEXT_PRIMARY,
                    ),
                    rx.spacer(),
                    rx.text(
                        FolderManagerState.tree_rows.length(),
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
                        FolderManagerState.tree_rows.length() > 0,
                        rx.vstack(
                            rx.foreach(FolderManagerState.tree_rows, _tree_row),
                            spacing="1",
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.icon("folder-plus", size=28, color=T.BORDER),
                                rx.text(
                                    "Chưa có thư mục nào.",
                                    font_size="0.85rem",
                                    color=T.TEXT_MUTED,
                                    text_align="center",
                                ),
                                rx.text(
                                    "Nhấn «Thêm thư mục con» để tạo thư mục đầu tiên.",
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
        on_mount=FolderManagerState.load_current_folder,
    )