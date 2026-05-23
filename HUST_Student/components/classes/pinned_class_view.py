"""
pinned_class_view.py — Nội dung chi tiết lớp đã ghim.

Hiển thị:
  • Breadcrumb + nút back
  • Các lớp con (có thể click để đi sâu)
  • Bài giảng trong lớp hiện tại
"""

import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.class_manager_state import ClassManagerState


# ── Breadcrumb navigation ─────────────────────────────────────────

def _breadcrumb_nav(pin_root_path: str):
    """Breadcrumb điều hướng từ root của lớp ghim."""
    parts = ClassManagerState.pinned_view_path.split("/")

    return rx.hstack(
        rx.icon("graduation-cap", size=14, color=T.SUCCESS),
        rx.hstack(
            # Nút back nếu đang ở sâu hơn root
            rx.cond(
                ClassManagerState.pinned_view_can_go_back,
                rx.hstack(
                    rx.box(
                        rx.icon("chevron-left", size=14, color=T.PRIMARY),
                        cursor="pointer",
                        on_click=ClassManagerState.navigate_pinned_back,
                        color=T.PRIMARY,
                        _hover={"color": T.PRIMARY_HOVER},
                        display="flex",
                        align_items="center",
                    ),
                    spacing="0",
                ),
                rx.box(),
            ),
            rx.text(
                ClassManagerState.pinned_view_breadcrumb,
                font_size="0.85rem",
                font_weight="700",
                color=T.TEXT_PRIMARY,
                no_of_lines=2,
            ),
            spacing="1",
            align="center",
        ),
        spacing="2",
        align="center",
        width="100%",
        padding="0.6rem 0.9rem",
        bg=T.BORDER_LIGHT,
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_MD,
    )


# ── Subclass card ─────────────────────────────────────────────────

def _subclass_card(item: dict):
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("graduation-cap", size=16, color=T.SUCCESS),
                bg="#E8F8F0",
                border_radius=T.RADIUS_MD,
                padding="0.45rem",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(
                    item["name"],
                    font_size="0.9rem",
                    font_weight="700",
                    color=T.TEXT_PRIMARY,
                    no_of_lines=1,
                ),
                rx.text(
                    item["subtitle"],
                    font_size="0.72rem",
                    color=T.TEXT_MUTED,
                    no_of_lines=1,
                ),
                spacing="0",
                align="start",
                flex="1",
                min_width="0",
            ),
            rx.cond(
                item["has_children"],
                rx.icon("chevron-right", size=15, color=T.TEXT_MUTED, flex_shrink="0"),
                rx.box(width="15px"),
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        width="100%",
        padding="0.75rem 1rem",
        bg=T.SURFACE,
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        cursor="pointer",
        transition="all 0.12s ease",
        on_click=ClassManagerState.navigate_pinned_into(item["path_key"]),
        _hover={
            "border_color": T.SUCCESS,
            "box_shadow": T.SHADOW_CARD_HOVER,
            "transform": "translateY(-1px)",
        },
    )


# ── Lesson card ───────────────────────────────────────────────────

def _lesson_card(item: dict):
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("book-open", size=15, color=T.PRIMARY),
                bg=T.PRIMARY_TINT,
                border_radius=T.RADIUS_SM,
                padding="0.4rem",
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
                    rx.icon("file-text", size=11, color=T.TEXT_MUTED),
                    rx.text(
                        item["terms_label"],
                        font_size="0.72rem",
                        color=T.TEXT_MUTED,
                    ),
                    spacing="1",
                    align="center",
                ),
                spacing="0",
                align="start",
                flex="1",
                min_width="0",
            ),
            rx.box(
                rx.icon("play", size=14, color=T.PRIMARY),
                bg=T.PRIMARY_TINT,
                border_radius="999px",
                padding="0.35rem",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        width="100%",
        padding="0.75rem 1rem",
        bg=T.SURFACE,
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        cursor="pointer",
        transition="all 0.12s ease",
        _hover={
            "border_color": T.PRIMARY,
            "box_shadow": T.SHADOW_CARD,
        },
    )


# ── Empty state ───────────────────────────────────────────────────

def _empty_box(icon: str, msg: str):
    return rx.box(
        rx.vstack(
            rx.icon(icon, size=24, color=T.BORDER),
            rx.text(msg, font_size="0.82rem", color=T.TEXT_MUTED, text_align="center"),
            spacing="2",
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
    )


# ── Main pinned class view ────────────────────────────────────────

def pinned_class_detail_view(pin_root_path: str):
    """
    View chi tiết lớp ghim. Truyền vào path gốc của lớp ghim.
    Hiển thị subclasses + lessons, có thể điều hướng vào sâu.
    """
    return rx.vstack(
        # Breadcrumb với back button
        _breadcrumb_nav(pin_root_path),

        # Subclasses section
        rx.cond(
            ClassManagerState.pinned_subclasses.length() > 0,
            rx.vstack(
                rx.hstack(
                    rx.icon("layers", size=14, color=T.SUCCESS),
                    rx.text(
                        "Lớp con",
                        font_size="0.82rem",
                        font_weight="700",
                        color=T.TEXT_SECONDARY,
                        text_transform="uppercase",
                        letter_spacing="0.06em",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.vstack(
                    rx.foreach(ClassManagerState.pinned_subclasses, _subclass_card),
                    spacing="2",
                    width="100%",
                ),
                spacing="2",
                width="100%",
                align="start",
            ),
            rx.box(),
        ),

        # Lessons section
        rx.vstack(
            rx.hstack(
                rx.icon("book-open", size=14, color=T.PRIMARY),
                rx.text(
                    "Bài giảng",
                    font_size="0.82rem",
                    font_weight="700",
                    color=T.TEXT_SECONDARY,
                    text_transform="uppercase",
                    letter_spacing="0.06em",
                ),
                spacing="2",
                align="center",
            ),
            rx.cond(
                ClassManagerState.pinned_view_lessons.length() > 0,
                rx.vstack(
                    rx.foreach(ClassManagerState.pinned_view_lessons, _lesson_card),
                    spacing="2",
                    width="100%",
                ),
                _empty_box("book-open", "Chưa có bài giảng trong lớp này"),
            ),
            spacing="2",
            width="100%",
            align="start",
        ),

        # Nếu không có cả subclass lẫn lesson
        rx.cond(
            (ClassManagerState.pinned_subclasses.length() == 0)
            & (ClassManagerState.pinned_view_lessons.length() == 0),
            _empty_box("graduation-cap", "Lớp này chưa có nội dung"),
            rx.box(),
        ),

        spacing="4",
        width="100%",
        align="start",
    )