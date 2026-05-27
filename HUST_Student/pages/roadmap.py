"""
roadmap.py — Trang quản lý lộ trình học.
Tương thích Reflex 0.9.
"""
import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.roadmap_state import RoadmapState, DayItem


# ══════════════════════════════════════════════════════════════════
# HELPER MODAL WRAPPER
# ══════════════════════════════════════════════════════════════════

def _simple_modal(title, show, close_fn, body, confirm_label, confirm_fn,
                  *, confirm_danger: bool = False):
    confirm_bg = T.DANGER if confirm_danger else T.PRIMARY
    confirm_hover = "#c0392b" if confirm_danger else T.PRIMARY_HOVER

    return rx.cond(
        show,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(title, font_size="1.1rem", font_weight="800",
                                color=T.TEXT_PRIMARY),
                        rx.spacer(),
                        modal_close_btn(close_fn),
                        width="100%", align="center",
                    ),
                    rx.divider(),
                    body,
                    rx.hstack(
                        rx.button("Hủy", on_click=close_fn,
                                  bg=T.BORDER_LIGHT, color=T.TEXT_PRIMARY,
                                  border_radius=T.RADIUS_MD, padding="0.5rem 1rem",
                                  font_weight="600", _hover={"bg": T.BORDER}),
                        rx.button(confirm_label, on_click=confirm_fn,
                                  bg=confirm_bg, color="white",
                                  border_radius=T.RADIUS_MD, padding="0.5rem 1rem",
                                  font_weight="700", _hover={"bg": confirm_hover}),
                        spacing="3", justify="end", width="100%",
                    ),
                    spacing="4", padding="1.5rem", width="100%",
                ),
                bg=T.SURFACE, border_radius=T.RADIUS_XL,
                width="460px", max_width="min(460px, calc(100vw - 2.5rem))",
                border=f"1px solid {T.BORDER}", box_shadow=T.SHADOW_MODAL,
                on_click=rx.stop_propagation,
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg=T.OVERLAY_SCRIM, z_index="1001", padding=T.MODAL_OVERLAY_PADDING,
            on_click=close_fn,
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# MODAL: ADD
# ══════════════════════════════════════════════════════════════════

def _add_modal():
    return _simple_modal(
        "Tạo lộ trình mới",
        RoadmapState.show_add,
        RoadmapState.close_add,
        rx.vstack(
            rx.vstack(
                rx.text("Tên lộ trình *", font_size="0.85rem",
                        font_weight="600", color=T.TEXT_PRIMARY),
                rx.input(
                    value=RoadmapState.new_title,
                    on_change=RoadmapState.set_new_title,
                    placeholder="Ví dụ: Tiếng Nhật N5 — 20 ngày",
                    auto_focus=True, width="100%",
                    border=f"1.5px solid {T.BORDER}", border_radius=T.RADIUS_MD,
                    _focus={"border_color": T.PRIMARY,
                            "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}"},
                ),
                spacing="2", width="100%",
            ),
            rx.vstack(
                rx.text("Số ngày học *", font_size="0.85rem",
                        font_weight="600", color=T.TEXT_PRIMARY),
                rx.input(
                    value=RoadmapState.new_total_days,
                    on_change=RoadmapState.set_new_total_days,
                    type="number", placeholder="20", width="100%",
                    border=f"1.5px solid {T.BORDER}", border_radius=T.RADIUS_MD,
                    _focus={"border_color": T.PRIMARY,
                            "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}"},
                ),
                rx.text(
                    "Lịch học được tự động tạo theo Spaced Repetition 4-cycle.",
                    font_size="0.75rem", color=T.TEXT_MUTED,
                ),
                spacing="1", width="100%",
            ),
            spacing="3", width="100%",
        ),
        "Tạo lộ trình", RoadmapState.confirm_add,
    )


# ══════════════════════════════════════════════════════════════════
# MODAL: EDIT
# ══════════════════════════════════════════════════════════════════

def _edit_modal():
    return _simple_modal(
        "Đổi tên lộ trình",
        RoadmapState.show_edit,
        RoadmapState.close_edit,
        rx.vstack(
            rx.text("Tên mới", font_size="0.85rem",
                    font_weight="600", color=T.TEXT_PRIMARY),
            rx.input(
                value=RoadmapState.edit_title,
                on_change=RoadmapState.set_edit_title,
                placeholder="Nhập tên mới...",
                auto_focus=True, width="100%",
                border=f"1.5px solid {T.BORDER}", border_radius=T.RADIUS_MD,
                _focus={"border_color": T.PRIMARY,
                        "box_shadow": f"0 0 0 3px {T.PRIMARY_LIGHT}"},
            ),
            spacing="2", width="100%",
        ),
        "Lưu", RoadmapState.confirm_edit,
    )


# ══════════════════════════════════════════════════════════════════
# MODAL: DELETE
# ══════════════════════════════════════════════════════════════════

def _delete_modal():
    return _simple_modal(
        "Xóa lộ trình",
        RoadmapState.show_delete,
        RoadmapState.close_delete,
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon("alert-triangle", size=20, color=T.DANGER),
                    bg=T.DANGER_BG, border_radius=T.RADIUS_MD, padding="0.5rem",
                    display="flex", align_items="center", justify_content="center",
                    flex_shrink="0",
                ),
                rx.vstack(
                    rx.text("Hành động này không thể hoàn tác!",
                            font_size="0.9rem", font_weight="700", color=T.DANGER),
                    rx.text(
                        "Lộ trình ", RoadmapState.delete_title,
                        " sẽ bị xóa vĩnh viễn.",
                        font_size="0.85rem", color=T.TEXT_SECONDARY,
                    ),
                    spacing="1", align="start",
                ),
                spacing="3", align="start", width="100%",
            ),
        ),
        "Xóa", RoadmapState.confirm_delete, confirm_danger=True,
    )


# ══════════════════════════════════════════════════════════════════
# MODAL: DETAIL — lịch từng ngày
# ══════════════════════════════════════════════════════════════════

def _day_row(day_item: DayItem):
    """Render 1 dòng ngày trong lịch. day_item là DayItem (pydantic BaseModel)."""
    return rx.box(
        rx.hstack(
            # Checkbox
            rx.box(
                rx.cond(
                    day_item.completed,
                    rx.icon("check", size=13, color="white"),
                    rx.box(),
                ),
                width="22px", height="22px",
                border_radius="6px",
                bg=rx.cond(day_item.completed, T.PRIMARY, T.SURFACE),
                border=rx.cond(
                    day_item.completed,
                    f"2px solid {T.PRIMARY}",
                    f"2px solid {T.BORDER}",
                ),
                display="flex", align_items="center", justify_content="center",
                cursor="pointer", flex_shrink="0",
                on_click=RoadmapState.toggle_day(
                    RoadmapState.detail_roadmap_id, day_item.day
                ),
                transition="all 0.15s ease",
                _hover={"border_color": T.PRIMARY},
            ),
            # Ngày
            rx.text(
                "Ngày ", day_item.day,
                font_size="0.78rem", font_weight="700",
                color=rx.cond(day_item.completed, T.PRIMARY, T.TEXT_MUTED),
                width="58px", flex_shrink="0",
            ),
            # Bài mới
            rx.hstack(
                rx.icon("book-open", size=12, color=T.PRIMARY),
                rx.text(
                    "Bài mới: ", day_item.new_lesson,
                    font_size="0.85rem", font_weight="600",
                    color=rx.cond(day_item.completed, T.TEXT_MUTED, T.TEXT_PRIMARY),
                    text_decoration=rx.cond(day_item.completed, "line-through", "none"),
                ),
                spacing="1", align="center",
            ),
            rx.spacer(),
            # Bài ôn
            rx.cond(
                day_item.has_reviews,
                rx.text(
                    "Ôn: ", day_item.review_str,
                    font_size="0.72rem", color=T.TEXT_MUTED,
                    no_of_lines=1, max_width="180px",
                ),
                rx.text("—", font_size="0.72rem", color=T.BORDER),
            ),
            spacing="3", align="center", width="100%",
        ),
        width="100%", padding="0.55rem 0.75rem",
        border_radius=T.RADIUS_MD,
        bg=rx.cond(day_item.completed, T.PRIMARY_TINT, T.SURFACE),
        border=rx.cond(
            day_item.completed,
            f"1px solid {T.PRIMARY_LIGHT}",
            f"1px solid {T.BORDER}",
        ),
        transition="all 0.12s ease",
        _hover={"border_color": T.PRIMARY},
    )


def _detail_modal():
    remaining = RoadmapState.detail_total_days - RoadmapState.detail_completed_count

    return rx.cond(
        RoadmapState.show_detail,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.text(RoadmapState.detail_title,
                                    font_size="1.15rem", font_weight="800",
                                    color=T.TEXT_PRIMARY, no_of_lines=2),
                            rx.hstack(
                                rx.badge(RoadmapState.detail_protocol,
                                         color_scheme="blue", variant="soft", size="1"),
                                spacing="2",
                            ),
                            spacing="1", align="start",
                        ),
                        rx.spacer(),
                        modal_close_btn(RoadmapState.close_detail),
                        width="100%", align="start",
                    ),
                    rx.divider(),

                    # Progress summary
                    rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text("Tổng ngày", font_size="0.72rem",
                                        color=T.TEXT_MUTED, font_weight="600"),
                                rx.text(RoadmapState.detail_total_days,
                                        font_size="1.4rem", font_weight="800",
                                        color=T.PRIMARY),
                                spacing="0", align="center",
                            ),
                            rx.box(width="1px", height="36px", bg=T.BORDER),
                            rx.vstack(
                                rx.text("Đã hoàn thành", font_size="0.72rem",
                                        color=T.TEXT_MUTED, font_weight="600"),
                                rx.text(RoadmapState.detail_completed_count,
                                        font_size="1.4rem", font_weight="800",
                                        color=T.SUCCESS),
                                spacing="0", align="center",
                            ),
                            rx.box(width="1px", height="36px", bg=T.BORDER),
                            rx.vstack(
                                rx.text("Còn lại", font_size="0.72rem",
                                        color=T.TEXT_MUTED, font_weight="600"),
                                rx.text(remaining, font_size="1.4rem",
                                        font_weight="800", color=T.WARN),
                                spacing="0", align="center",
                            ),
                            spacing="6", justify="center", width="100%",
                        ),
                        padding="0.9rem 1rem", bg=T.BORDER_LIGHT,
                        border_radius=T.RADIUS_MD, width="100%",
                    ),

                    # Schedule list
                    rx.text("Lịch học chi tiết",
                            font_size="0.85rem", font_weight="700",
                            color=T.TEXT_PRIMARY),
                    rx.box(
                        rx.vstack(
                            rx.foreach(RoadmapState.detail_schedule, _day_row),
                            spacing="2", width="100%",
                        ),
                        width="100%", max_height="380px",
                        overflow_y="auto", padding_right="4px",
                    ),

                    spacing="4", padding="1.75rem 2rem 2rem", width="100%",
                ),
                bg=T.SURFACE, border_radius=T.RADIUS_XL,
                width="620px", max_width="min(620px, calc(100vw - 2.5rem))",
                max_height=T.MODAL_CONTENT_MAX_HEIGHT,
                min_height="0", overflow_y="auto", overflow_x="hidden",
                border=f"1px solid {T.BORDER}", box_shadow=T.SHADOW_MODAL,
                on_click=rx.stop_propagation,
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg=T.OVERLAY_SCRIM, z_index="1001", padding=T.MODAL_OVERLAY_PADDING,
            on_click=RoadmapState.close_detail,
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# ROADMAP CARD — render từ dict
# ══════════════════════════════════════════════════════════════════

def _roadmap_card(r: dict):
    rid = r["id"]
    title = r["title"]
    total = r["total_days"]
    protocol = r["protocol"]
    
    # Read the pre-calculated values directly from the frontend Var
    completed = r["completed_count"]
    pct = r["pct"]

    return rx.box(
        rx.vstack(
            # Title + actions
            rx.hstack(
                rx.icon("map", size=15, color=T.PRIMARY, flex_shrink="0"),
                rx.text(
                    title, font_size="0.95rem", font_weight="700",
                    color=T.TEXT_PRIMARY, flex="1", no_of_lines=2,
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("pencil", size=13),
                        on_click=RoadmapState.open_edit(rid, title),
                        bg="transparent", color=T.TEXT_MUTED, padding="0.3rem",
                        border_radius=T.RADIUS_SM,
                        _hover={"bg": T.PRIMARY_TINT, "color": T.PRIMARY},
                    ),
                    rx.button(
                        rx.icon("trash-2", size=13),
                        on_click=RoadmapState.open_delete(rid, title),
                        bg="transparent", color=T.TEXT_MUTED, padding="0.3rem",
                        border_radius=T.RADIUS_SM,
                        _hover={"bg": T.DANGER_BG, "color": T.DANGER},
                    ),
                    spacing="0", flex_shrink="0",
                ),
                spacing="2", align="start", width="100%",
            ),

            # Protocol badge
            rx.badge(protocol, color_scheme="blue", variant="soft", size="1"),

            # Progress
            rx.vstack(
                rx.hstack(
                    rx.text(
                        f"{completed} / {total} ngày",
                        font_size="0.75rem", font_weight="700",
                        color=T.TEXT_SECONDARY,
                    ),
                    rx.spacer(),
                    rx.text(
                        f"{pct}%",
                        font_size="0.75rem", font_weight="700", color=T.PRIMARY,
                    ),
                    width="100%", align="center",
                ),
                rx.box(
                    rx.box(
                        height="100%",
                        width=f"{pct}%",
                        bg=T.PRIMARY,
                        border_radius="999px",
                        transition="width 0.4s ease",
                    ),
                    width="100%", height="5px",
                    bg=T.BORDER_LIGHT, border_radius="999px", overflow="hidden",
                ),
                spacing="1", width="100%",
            ),

            # View detail
            rx.button(
                rx.hstack(
                    rx.icon("calendar", size=13),
                    rx.text("Xem lịch học", font_size="0.82rem", font_weight="600"),
                    spacing="2", align="center",
                ),
                on_click=RoadmapState.open_detail(rid),
                bg=T.PRIMARY_TINT, color=T.PRIMARY,
                border=f"1px solid {T.PRIMARY_LIGHT}",
                border_radius=T.RADIUS_MD, width="100%", padding="0.55rem",
                _hover={"bg": T.PRIMARY, "color": "white"},
                transition="all 0.15s ease",
            ),

            spacing="3", align="start", width="100%",
        ),
        padding="1.1rem 1.25rem",
        bg=T.SURFACE, border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG, box_shadow=T.SHADOW_CARD,
        transition="all 0.12s ease",
        _hover={"border_color": T.PRIMARY, "box_shadow": T.SHADOW_CARD_HOVER},
        width="100%",
    )


# ══════════════════════════════════════════════════════════════════
# TOAST
# ══════════════════════════════════════════════════════════════════

def _toast():
    return rx.cond(
        RoadmapState.message != "",
        rx.box(
            rx.hstack(
                rx.icon(
                    rx.cond(RoadmapState.message_type == "error",
                            "alert-circle", "check-circle"),
                    size=16,
                    color=rx.cond(RoadmapState.message_type == "error",
                                  T.DANGER, T.SUCCESS),
                    flex_shrink="0",
                ),
                rx.text(RoadmapState.message, font_size="0.85rem",
                        font_weight="500", flex="1",
                        color=rx.cond(RoadmapState.message_type == "error",
                                      T.DANGER, T.SUCCESS)),
                rx.button(
                    rx.icon("x", size=14),
                    on_click=RoadmapState.clear_message,
                    bg="transparent", padding="0.2rem", color=T.TEXT_MUTED,
                    _hover={"color": T.TEXT_PRIMARY}, flex_shrink="0",
                ),
                width="100%", spacing="2", align="center",
            ),
            width="100%", padding="0.65rem 0.9rem", border_radius=T.RADIUS_MD,
            bg=rx.cond(RoadmapState.message_type == "error", T.DANGER_BG, T.SUCCESS_BG),
            border=rx.cond(RoadmapState.message_type == "error",
                           f"1px solid {T.DANGER}", f"1px solid {T.SUCCESS}"),
        ),
        rx.box(),
    )


# ══════════════════════════════════════════════════════════════════
# MAIN PAGE
# ══════════════════════════════════════════════════════════════════

def roadmap_page():
    return rx.vstack(
        _add_modal(),
        _edit_modal(),
        _delete_modal(),
        _detail_modal(),

        # Header
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.icon("map", size=18, color=T.PRIMARY),
                    rx.text("Lộ trình học", font_size="1.35rem",
                            font_weight="800", color=T.TEXT_PRIMARY,
                            letter_spacing="-0.02em"),
                    spacing="2", align="center",
                ),
                rx.text(
                    "Tạo và theo dõi lộ trình học theo phương pháp Spaced Repetition.",
                    font_size="0.85rem", color=T.TEXT_SECONDARY,
                ),
                spacing="1", align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=14),
                    rx.text("Tạo lộ trình", font_size="0.875rem", font_weight="600"),
                    spacing="2", align="center",
                ),
                on_click=RoadmapState.open_add,
                bg=T.PRIMARY, color="white",
                border_radius=T.RADIUS_MD,
                padding_x="1rem", height="36px",
                _hover={"bg": T.PRIMARY_HOVER},
            ),
            width="100%", align="center",
        ),

        _toast(),

        # Cards
        rx.cond(
            RoadmapState.roadmap_count > 0,
            rx.grid(
                rx.foreach(RoadmapState.roadmaps, _roadmap_card),
                template_columns="repeat(2, minmax(0, 1fr))",
                gap="4", width="100%",
            ),
            rx.box(
                rx.vstack(
                    rx.icon("map", size=36, color=T.BORDER),
                    rx.text("Chưa có lộ trình nào.",
                            font_size="0.9rem", color=T.TEXT_MUTED,
                            text_align="center"),
                    rx.text("Nhấn «Tạo lộ trình» để bắt đầu.",
                            font_size="0.8rem", color=T.TEXT_MUTED,
                            text_align="center"),
                    spacing="2", align="center",
                ),
                padding="3rem", width="100%",
                display="flex", align_items="center", justify_content="center",
                bg=T.SURFACE, border=f"1px dashed {T.BORDER}",
                border_radius=T.RADIUS_LG,
            ),
        ),

        spacing="4", width="100%", height="100%", align="start",
        on_mount=RoadmapState.load_roadmaps,
    )