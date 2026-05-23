import reflex as rx

from HUST_Student.components.classes.class_manager_panel import class_manager_panel
from HUST_Student.components.ui import theme as T
from HUST_Student.states.class_manager_state import ClassManagerState
from HUST_Student.states.kanji_state import ClassesTabState


# ─────────────────────────────────────────────────────────────────
# TAB BUTTON
# ─────────────────────────────────────────────────────────────────

def _tab(label: str, icon: str, active, on_click):
    return rx.hstack(
        rx.icon(icon, size=15, color=rx.cond(active, T.PRIMARY, T.TEXT_MUTED)),
        rx.text(
            label,
            font_weight=rx.cond(active, "700", "500"),
            font_size="0.875rem",
            color=rx.cond(active, T.PRIMARY, T.TEXT_SECONDARY),
        ),
        spacing="2", align="center",
        padding="0.55rem 1rem",
        border_radius=T.RADIUS_MD,
        bg=rx.cond(active, T.PRIMARY_TINT, "transparent"),
        border=rx.cond(active, f"1.5px solid {T.PRIMARY_LIGHT}", "1.5px solid transparent"),
        cursor="pointer",
        transition="all 0.12s ease",
        on_click=on_click,
        _hover={"bg": T.PRIMARY_TINT},
        flex_shrink="0",
    )


def _pinned_tab(item: dict):
    """Tab động cho lớp đã ghim — có nút × để bỏ ghim."""
    is_active = ClassManagerState.selected_path_key == item["path_key"]
    return rx.hstack(
        rx.icon("graduation-cap", size=13,
                color=rx.cond(is_active, T.PRIMARY, T.TEXT_MUTED)),
        rx.text(
            item["name"],
            font_weight=rx.cond(is_active, "700", "500"),
            font_size="0.875rem",
            color=rx.cond(is_active, T.PRIMARY, T.TEXT_SECONDARY),
            max_width="120px",
            no_of_lines=1,
        ),
        # Nút bỏ ghim
        rx.box(
            rx.icon("x", size=11),
            on_click=[
                ClassManagerState.unpin_class(item["pin_key"]),
                rx.stop_propagation,
            ],
            color=rx.cond(is_active, T.PRIMARY, T.TEXT_MUTED),
            padding="0.1rem",
            border_radius="999px",
            cursor="pointer",
            _hover={"color": T.DANGER, "bg": T.DANGER_BG},
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        spacing="1", align="center",
        padding="0.55rem 0.75rem",
        border_radius=T.RADIUS_MD,
        bg=rx.cond(is_active, T.PRIMARY_TINT, "transparent"),
        border=rx.cond(is_active,
                       f"1.5px solid {T.PRIMARY_LIGHT}",
                       "1.5px solid transparent"),
        cursor="pointer",
        transition="all 0.12s ease",
        on_click=[
            ClassManagerState.select_class(item["path_key"]),
            ClassesTabState.set_tab("lop_hoc"),
        ],
        _hover={"bg": T.PRIMARY_TINT},
        flex_shrink="0",
    )


# ─────────────────────────────────────────────────────────────────
# MAIN classes_page
# ─────────────────────────────────────────────────────────────────

def classes_page():
    is_classes_tab = ClassesTabState.active_tab == "lop_hoc"

    return rx.vstack(
        # ── Header ──────────────────────────────────────────────
        rx.hstack(
            rx.vstack(
                rx.text(
                    "Lớp học",
                    font_size="1.5rem", font_weight="800",
                    color=T.TEXT_PRIMARY, letter_spacing="-0.02em",
                ),
                rx.text(
                    "Quản lý lớp học, thêm bài giảng và ghim lớp hay dùng",
                    font_size="0.85rem", color=T.TEXT_SECONDARY,
                ),
                spacing="0", align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon("folder-plus", size=14),
                    rx.text("Thêm lớp gốc", font_size="0.85rem", font_weight="600"),
                    spacing="2", align="center",
                ),
                on_click=ClassManagerState.open_add_subclass_dialog,
                bg=T.PRIMARY, color="white",
                border_radius=T.RADIUS_MD,
                padding_x="1rem", height="36px",
                _hover={"bg": T.PRIMARY_HOVER},
            ),
            width="100%", align="center",
        ),

        # ── Tabs: "Quản lý lớp" + pinned class tabs ─────────────
        rx.hstack(
            _tab(
                "Quản lý lớp", "graduation-cap",
                is_classes_tab,
                ClassesTabState.set_tab("lop_hoc"),
            ),
            # Tab động cho từng lớp đã ghim
            rx.foreach(ClassManagerState.pinned_classes, _pinned_tab),
            spacing="2",
            border_bottom=f"1px solid {T.BORDER_LIGHT}",
            padding_bottom="0.5rem",
            width="100%",
            overflow_x="auto",
            flex_wrap="nowrap",
        ),

        rx.divider(margin_y="0"),

        # ── Content ─────────────────────────────────────────────
        rx.box(
            class_manager_panel(),
            width="100%",
            flex="1",
            overflow_y="auto",
        ),

        spacing="4", width="100%", height="100%", align="start",
    )