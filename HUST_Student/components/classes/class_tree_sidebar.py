"""Cây lớp học bên trái — reactive."""

import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.class_manager_state import ClassManagerState
from HUST_Student.states.kanji_state import ClassTreeState


def _class_row(row: dict):
    is_open = ClassTreeState.open_classes.contains(row["tree_key"])
    is_active = ClassTreeState.current_path_key == row["path_key"]

    return rx.box(
        rx.hstack(
            rx.box(width=row["indent_px"], flex_shrink="0"),
            rx.cond(
                is_open,
                rx.icon("chevron-down", size=12, color=T.TEXT_MUTED),
                rx.icon("chevron-right", size=12, color=T.TEXT_MUTED),
            ),
            rx.icon("graduation-cap", size=14, color=T.PRIMARY),
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
        padding="0.45rem 0.6rem",
        border_radius=T.RADIUS_MD,
        cursor="pointer",
        bg=rx.cond(is_active, T.PRIMARY_TINT, "transparent"),
        on_click=[
            ClassTreeState.toggle_class(row["tree_key"]),
            ClassTreeState.set_active_path(row["path_key"]),
            ClassManagerState.apply_selection(row["path_key"]),
        ],
    )


def _lesson_row(row: dict):
    return rx.box(
        rx.hstack(
            rx.box(width=row["indent_px"], flex_shrink="0"),
            rx.icon("book-open", size=12, color=T.PRIMARY),
            rx.text(
                row["title"],
                font_size="0.8rem",
                color=T.TEXT_SECONDARY,
                flex="1",
                no_of_lines=1,
            ),
            spacing="2",
            align="center",
            width="100%",
            padding="0.3rem 0.5rem",
        ),
        width="100%",
        padding_left="0.25rem",
        cursor="pointer",
        on_click=ClassManagerState.apply_selection(row["path_key"]),
    )


def _sidebar_row(row: dict):
    return rx.cond(
        row["row_type"] == "class",
        _class_row(row),
        _lesson_row(row),
    )


def class_sidebar_tree():
    return rx.vstack(
        rx.foreach(ClassTreeState.visible_sidebar_rows, _sidebar_row),
        spacing="0",
        width="100%",
    )
