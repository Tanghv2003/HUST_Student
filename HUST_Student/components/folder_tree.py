"""
folder_tree.py — Cây thư mục trong sidebar (reactive).

Sidebar tree hiển thị:
  • Folder rows: có thể click để toggle mở/đóng & chọn folder
  • Studyset rows: click để vào học phần
"""

import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.folder_manager_state import FolderManagerState
from HUST_Student.states.folder_state import FolderState
from HUST_Student.states.navigation_state import NavigationState
from HUST_Student.states.tree_state import TreeState


# ══════════════════════════════════════════════════════════════════
# FOLDER ROW
# ══════════════════════════════════════════════════════════════════

def _folder_header(row: dict):
    is_open = TreeState.open_folders.contains(row["tree_key"])
    is_active = NavigationState.current_path_key == row["path_key"]

    return rx.box(
        rx.hstack(
            rx.box(width=row["indent_px"], flex_shrink="0"),
            # Chevron
            rx.cond(
                row["has_children"],
                rx.cond(
                    is_open,
                    rx.icon("chevron-down", size=12, color=T.TEXT_MUTED),
                    rx.icon("chevron-right", size=12, color=T.TEXT_MUTED),
                ),
                rx.box(width="12px", flex_shrink="0"),
            ),
            # Folder icon
            rx.cond(
                is_open,
                rx.icon("folder-open", size=15, color=T.WARN),
                rx.icon("folder", size=15, color=T.WARN),
            ),
            # Name
            rx.text(
                row["name"],
                font_weight=rx.cond(is_active, "700", "600"),
                color=rx.cond(is_active, T.PRIMARY, T.TEXT_PRIMARY),
                font_size="0.875rem",
                flex="1",
                no_of_lines=1,
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        width="100%",
        padding="0.5rem 0.65rem",
        border_radius=T.RADIUS_MD,
        cursor="pointer",
        bg=rx.cond(is_active, T.PRIMARY_TINT, "transparent"),
        transition="background 0.12s ease",
        on_click=[
            TreeState.toggle_folder(row["tree_key"]),
            FolderState.open_folder_path(row["path_key"]),
            NavigationState.set_active_path(row["path_key"]),
            FolderManagerState.apply_selection(row["path_key"]),
        ],
        _hover=rx.cond(is_active, {}, {"bg": T.BORDER_LIGHT}),
    )


# ══════════════════════════════════════════════════════════════════
# STUDYSET ROW
# ══════════════════════════════════════════════════════════════════

def _studyset_row(row: dict):
    return rx.box(
        rx.hstack(
            rx.box(width=row["indent_px"], flex_shrink="0"),
            rx.icon("book-open", size=12, color=T.PRIMARY),
            rx.text(
                row["title"],
                font_size="0.8rem",
                font_weight="500",
                color=T.TEXT_SECONDARY,
                flex="1",
                no_of_lines=1,
            ),
            rx.text(
                row["terms"],
                font_size="0.65rem",
                color=T.TEXT_MUTED,
                flex_shrink="0",
            ),
            spacing="2",
            align="center",
            width="100%",
            padding="0.35rem 0.5rem",
        ),
        width="100%",
        padding_left="0.4rem",
        cursor="pointer",
        border_radius=T.RADIUS_SM,
        transition="background 0.1s ease",
        on_click=[
            FolderState.open_folder_path(row["path_key"]),
            FolderState.select_set(row["title"]),
            NavigationState.set_folder_detail_path(row["path_key"]),
            FolderManagerState.apply_selection(row["path_key"]),
        ],
        _hover={"bg": T.PRIMARY_TINT},
    )


# ══════════════════════════════════════════════════════════════════
# ROW DISPATCHER
# ══════════════════════════════════════════════════════════════════

def sidebar_tree_row(row: dict):
    return rx.cond(
        row["row_type"] == "folder",
        _folder_header(row),
        _studyset_row(row),
    )


# ══════════════════════════════════════════════════════════════════
# MAIN TREE COMPONENT
# ══════════════════════════════════════════════════════════════════

def sidebar_folder_tree():
    return rx.cond(
        TreeState.visible_sidebar_rows.length() > 0,
        rx.vstack(
            rx.foreach(TreeState.visible_sidebar_rows, sidebar_tree_row),
            spacing="0",
            width="100%",
        ),
        rx.box(
            rx.text(
                "Chưa có thư mục",
                font_size="0.8rem",
                color=T.TEXT_MUTED,
                text_align="center",
                padding="1rem",
            ),
        ),
    )