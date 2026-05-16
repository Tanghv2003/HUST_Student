"""
folder_tree.py — Cây thư mục với studysets hiển thị inline (accordion).

- Click folder → mở/đóng, đồng thời navigate tới folder_detail.
- Khi mở, studysets xuất hiện ngay bên dưới folder.
- Key trong open_folders: "name::path" để tránh trùng tên folder.
"""

import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.services.studyset_service import load_studysets
from HUST_Student.states.folder_state import FolderState
from HUST_Student.states.navigation_state import NavigationState
from HUST_Student.states.tree_state import TreeState


# ─────────────────────────────────────────────────────────────────

def _studyset_pill(title: str, terms: int, folder_name: str):
    """Studyset nhỏ gọn hiển thị ngay trong cây."""
    return rx.hstack(
        rx.box(
            width="2px",
            min_height="28px",
            bg=T.PRIMARY_LIGHT,
            border_radius="999px",
            flex_shrink="0",
        ),
        rx.hstack(
            rx.icon("book-open", size=12, color=T.PRIMARY),
            rx.text(
                title,
                font_size="0.8rem",
                font_weight="500",
                color=T.TEXT_SECONDARY,
                flex="1",
                no_of_lines=1,
            ),
            rx.box(
                rx.text(f"{terms}", font_size="0.65rem", color=T.TEXT_MUTED, line_height="1"),
                bg=T.BORDER_LIGHT,
                padding="0.1rem 0.4rem",
                border_radius="999px",
            ),
            spacing="2",
            align="center",
            width="100%",
            padding="0.35rem 0.5rem",
            border_radius=T.RADIUS_MD,
            cursor="pointer",
            transition="background 0.12s",
            _hover={"bg": T.PRIMARY_TINT, "color": T.PRIMARY},
            on_click=lambda: [
                FolderState.open_folder(folder_name),
                FolderState.select_set(title),
                NavigationState.set_folder_detail(folder_name),
            ],
        ),
        spacing="2",
        align="stretch",
        width="100%",
        padding_left="0.4rem",
    )


def _load_sets(folder_path: str) -> list[dict]:
    try:
        return load_studysets().get(folder_path, [])
    except Exception:
        return []


def folder_node(name: str, data: dict, level: int = 0, parent_path: str = ""):
    sub_folders = data.get("folders", {})
    folder_path = f"{parent_path}/{name}" if parent_path else name
    tree_key = f"{name}::{folder_path}"
    sets_data = _load_sets(folder_path)
    indent = level * 14

    has_content = bool(sub_folders) or bool(sets_data)

    is_open = TreeState.open_folders.contains(tree_key)
    is_active = NavigationState.current_folder == name

    # ── Header row ─────────────────────────────────────────
    header = rx.hstack(
        rx.box(width=f"{indent}px", flex_shrink="0") if indent > 0 else rx.fragment(),
        rx.hstack(
            # chevron
            rx.cond(
                has_content,
                rx.cond(
                    is_open,
                    rx.icon("chevron-down", size=12, color=T.TEXT_MUTED),
                    rx.icon("chevron-right", size=12, color=T.TEXT_MUTED),
                ),
                rx.box(width="12px"),
            ),
            # folder icon
            rx.cond(
                is_open,
                rx.icon("folder-open", size=15, color=T.WARN),
                rx.icon("folder", size=15, color=T.WARN),
            ),
            rx.text(
                name,
                font_weight=rx.cond(is_active, "700", "600"),
                color=rx.cond(is_active, T.PRIMARY, T.TEXT_PRIMARY),
                font_size="0.875rem",
                flex="1",
                no_of_lines=1,
            ),
            spacing="2",
            align="center",
            flex="1",
            padding="0.5rem 0.65rem",
            border_radius=T.RADIUS_MD,
            cursor="pointer",
            bg=rx.cond(is_active, T.PRIMARY_TINT, "transparent"),
            transition="background 0.12s",
            _hover={"bg": T.PRIMARY_TINT},
            on_click=lambda: [
                TreeState.toggle_folder(tree_key),
                FolderState.open_folder(name),
                NavigationState.set_folder_detail(name),
            ],
        ),
        spacing="0",
        align="center",
        width="100%",
    )

    # ── Inline studysets ────────────────────────────────────
    set_rows = (
        rx.vstack(
            *[_studyset_pill(s["title"], s.get("terms", 0), name) for s in sets_data],
            spacing="0",
            width="100%",
            padding_left=f"{indent + 22}px",
            padding_top="0.1rem",
            padding_bottom="0.25rem",
        )
        if sets_data
        else rx.box()
    )

    # ── Sub-folders ─────────────────────────────────────────
    sub_nodes = (
        rx.vstack(
            *[
                folder_node(child_name, child_data, level + 1, folder_path)
                for child_name, child_data in sub_folders.items()
            ],
            spacing="0",
            width="100%",
        )
        if sub_folders
        else rx.box()
    )

    expanded = rx.cond(
        is_open,
        rx.vstack(set_rows, sub_nodes, spacing="0", width="100%"),
        rx.box(),
    )

    return rx.vstack(header, expanded, spacing="0", align="start", width="100%")