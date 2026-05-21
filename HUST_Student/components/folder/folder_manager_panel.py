import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_manager_state import FolderManagerState


def _action_btn(icon: str, label: str, on_click, *, danger: bool = False):
    return rx.button(
        rx.icon(icon, size=14),
        rx.text(label, font_size="0.8rem", font_weight="600"),
        on_click=on_click,
        bg=T.DANGER_BG if danger else T.SURFACE,
        color=T.DANGER if danger else T.TEXT_PRIMARY,
        border=f"1px solid {T.DANGER if danger else T.BORDER}",
        border_radius=T.RADIUS_MD,
        padding="0.45rem 0.75rem",
        _hover={"bg": "#fde0e0" if danger else T.PRIMARY_TINT},
    )


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
        on_click=FolderManagerState.select_folder(row["path_key"]),
    )


def _simple_modal(title: str, show, close_fn, body, confirm_label: str, confirm_fn):
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
                        ),
                        rx.button(
                            confirm_label,
                            on_click=confirm_fn,
                            bg=T.PRIMARY,
                            color="white",
                            border_radius=T.RADIUS_MD,
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
                width="440px",
                max_width="min(440px, calc(100vw - 2.5rem))",
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
            z_index="999",
            padding=T.MODAL_OVERLAY_PADDING,
            on_click=close_fn,
        ),
        rx.box(),
    )


def _rename_modal():
    return _simple_modal(
        "Đổi tên thư mục",
        FolderManagerState.show_rename_dialog,
        FolderManagerState.close_rename_dialog,
        rx.input(
            placeholder="Tên thư mục mới",
            value=FolderManagerState.new_folder_name,
            on_change=FolderManagerState.set_new_folder_name,
            width="100%",
        ),
        "Lưu",
        FolderManagerState.confirm_rename_folder,
    )


def _add_subfolder_modal():
    return _simple_modal(
        "Thêm thư mục con",
        FolderManagerState.show_add_subfolder_dialog,
        FolderManagerState.close_add_subfolder_dialog,
        rx.vstack(
            rx.text(FolderManagerState.breadcrumb, font_size="0.8rem", color=T.TEXT_MUTED),
            rx.input(
                placeholder="Tên thư mục *",
                value=FolderManagerState.new_subfolder_name,
                on_change=FolderManagerState.set_new_subfolder_name,
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        "Thêm",
        FolderManagerState.confirm_add_subfolder,
    )


def _delete_modal():
    return _simple_modal(
        "Xóa thư mục",
        FolderManagerState.show_delete_confirmation,
        FolderManagerState.close_delete_confirmation,
        rx.text(
            "Xóa thư mục này, mọi thư mục con và bài giảng bên trong?",
            color=T.TEXT_SECONDARY,
            font_size="0.9rem",
        ),
        "Xóa",
        FolderManagerState.confirm_delete_folder,
    )


def _add_studyset_modal():
    return _simple_modal(
        "Thêm bài giảng",
        FolderManagerState.show_add_studyset_dialog,
        FolderManagerState.close_add_studyset_dialog,
        rx.vstack(
            rx.text(FolderManagerState.breadcrumb, font_size="0.8rem", color=T.TEXT_MUTED),
            rx.input(
                placeholder="Tên bài giảng *",
                value=FolderManagerState.new_studyset_title,
                on_change=FolderManagerState.set_new_studyset_title,
                width="100%",
            ),
            rx.input(
                placeholder="File JSON * (vd: nihongo/kanji/Kanji_N5.json)",
                value=FolderManagerState.new_studyset_file,
                on_change=FolderManagerState.set_new_studyset_file,
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        "Thêm",
        FolderManagerState.confirm_add_studyset,
    )


def _studyset_row(item: dict):
    return rx.box(
        rx.hstack(
            rx.icon("book-open", size=14, color=T.PRIMARY),
            rx.vstack(
                rx.text(item["title"], font_size="0.85rem", font_weight="600", color=T.TEXT_PRIMARY),
                rx.text(item["file"], font_size="0.72rem", color=T.TEXT_MUTED, no_of_lines=1),
                spacing="0",
                align="start",
                flex="1",
            ),
            rx.text(item["terms_label"], font_size="0.7rem", color=T.TEXT_MUTED),
            rx.button(
                rx.icon("trash-2", size=14),
                on_click=FolderManagerState.remove_studyset_item(item["title"]),
                bg="transparent",
                color=T.DANGER,
                padding="0.25rem",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        width="100%",
        padding="0.55rem 0.7rem",
        bg=T.SURFACE,
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_MD,
    )


def folder_manager_panel():
    return rx.box(
        _rename_modal(),
        _add_subfolder_modal(),
        _add_studyset_modal(),
        _delete_modal(),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("Quản lý thư mục", font_size="1rem", font_weight="700", color=T.TEXT_PRIMARY),
                    rx.text(
                        "Folder chứa thư mục con hoặc bài giảng (JSON)",
                        font_size="0.78rem",
                        color=T.TEXT_MUTED,
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.spacer(),
                rx.button(
                    "Gốc",
                    on_click=FolderManagerState.select_folder(""),
                    bg=rx.cond(FolderManagerState.is_at_root, T.PRIMARY, T.BORDER_LIGHT),
                    color=rx.cond(FolderManagerState.is_at_root, "white", T.TEXT_PRIMARY),
                    border_radius=T.RADIUS_MD,
                    size="2",
                ),
                width="100%",
                align="center",
            ),
            rx.box(
                rx.text("Đang chọn", font_size="0.72rem", color=T.TEXT_MUTED),
                rx.text(
                    FolderManagerState.breadcrumb,
                    font_size="0.9rem",
                    font_weight="600",
                    color=T.TEXT_PRIMARY,
                ),
                rx.text(
                    FolderManagerState.folder_summary,
                    font_size="0.78rem",
                    color=T.TEXT_SECONDARY,
                ),
                width="100%",
                padding="0.65rem 0.85rem",
                bg=T.BORDER_LIGHT,
                border_radius=T.RADIUS_MD,
            ),
            rx.cond(
                FolderManagerState.message != "",
                rx.box(
                    rx.hstack(
                        rx.text(FolderManagerState.message, font_size="0.85rem", flex="1"),
                        rx.button(
                            rx.icon("x", size=14),
                            on_click=FolderManagerState.clear_message,
                            bg="transparent",
                            padding="0",
                        ),
                        width="100%",
                    ),
                    width="100%",
                    padding="0.6rem 0.85rem",
                    border_radius=T.RADIUS_MD,
                    bg=rx.cond(
                        FolderManagerState.message_type == "error",
                        T.DANGER_BG,
                        T.SUCCESS_BG,
                    ),
                ),
                rx.box(),
            ),
            rx.grid(
                _action_btn("folder-plus", "Thêm con", FolderManagerState.open_add_subfolder_dialog),
                _action_btn("pencil", "Đổi tên", FolderManagerState.open_rename_dialog),
                _action_btn("book-plus", "Bài giảng", FolderManagerState.open_add_studyset_dialog),
                _action_btn("trash-2", "Xóa", FolderManagerState.open_delete_confirmation, danger=True),
                grid_template_columns="repeat(2, 1fr)",
                gap="2",
                width="100%",
            ),
            rx.cond(
                FolderManagerState.is_at_root == False,
                rx.vstack(
                    rx.text(
                        "Bài giảng (studysets.json)",
                        font_size="0.85rem",
                        font_weight="600",
                        color=T.TEXT_PRIMARY,
                    ),
                    rx.cond(
                        FolderManagerState.folder_studysets.length() > 0,
                        rx.vstack(
                            rx.foreach(FolderManagerState.folder_studysets, _studyset_row),
                            spacing="2",
                            width="100%",
                        ),
                        rx.text(
                            "Chưa có bài giảng. Nhấn «Bài giảng» để thêm file JSON.",
                            font_size="0.8rem",
                            color=T.TEXT_MUTED,
                        ),
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.box(),
            ),
            rx.box(
                rx.cond(
                    FolderManagerState.tree_rows.length() > 0,
                    rx.vstack(
                        rx.foreach(FolderManagerState.tree_rows, _tree_row),
                        spacing="1",
                        width="100%",
                    ),
                    rx.text(
                        "Chưa có thư mục. Chọn «Gốc» rồi nhấn «Thêm con».",
                        color=T.TEXT_MUTED,
                        font_size="0.85rem",
                        text_align="center",
                        padding="2rem",
                    ),
                ),
                width="100%",
                max_height="420px",
                overflow_y="auto",
                border=f"1px solid {T.BORDER}",
                border_radius=T.RADIUS_LG,
                padding="0.5rem",
                bg=T.SURFACE,
            ),
            spacing="3",
            width="100%",
            align="start",
        ),
        width="100%",
        on_mount=FolderManagerState.load_current_folder,
    )
