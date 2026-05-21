import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.class_manager_state import ClassManagerState


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
    is_selected = ClassManagerState.selected_path_key == row["path_key"]

    return rx.box(
        rx.hstack(
            rx.box(width=row["indent_px"], flex_shrink="0"),
            rx.icon("graduation-cap", size=15, color=T.PRIMARY, flex_shrink="0"),
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
        on_click=ClassManagerState.select_class(row["path_key"]),
    )


def _simple_modal(title, show, close_fn, body, confirm_label, confirm_fn):
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
                        rx.button("Hủy", on_click=close_fn, bg=T.BORDER_LIGHT, border_radius=T.RADIUS_MD),
                        rx.button(confirm_label, on_click=confirm_fn, bg=T.PRIMARY, color="white", border_radius=T.RADIUS_MD),
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


def _lesson_row(item: dict):
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
                on_click=ClassManagerState.remove_lesson_item(item["title"]),
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


def class_manager_panel():
    return rx.box(
        _simple_modal(
            "Đổi tên lớp",
            ClassManagerState.show_rename_dialog,
            ClassManagerState.close_rename_dialog,
            rx.input(
                placeholder="Tên lớp mới",
                value=ClassManagerState.new_class_name,
                on_change=ClassManagerState.set_new_class_name,
                width="100%",
            ),
            "Lưu",
            ClassManagerState.confirm_rename_class,
        ),
        _simple_modal(
            "Thêm lớp con",
            ClassManagerState.show_add_subclass_dialog,
            ClassManagerState.close_add_subclass_dialog,
            rx.vstack(
                rx.text(ClassManagerState.breadcrumb, font_size="0.8rem", color=T.TEXT_MUTED),
                rx.input(
                    placeholder="Tên lớp con *",
                    value=ClassManagerState.new_subclass_name,
                    on_change=ClassManagerState.set_new_subclass_name,
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            "Thêm",
            ClassManagerState.confirm_add_subclass,
        ),
        _simple_modal(
            "Thêm bài giảng",
            ClassManagerState.show_add_lesson_dialog,
            ClassManagerState.close_add_lesson_dialog,
            rx.vstack(
                rx.text(ClassManagerState.breadcrumb, font_size="0.8rem", color=T.TEXT_MUTED),
                rx.input(
                    placeholder="Tên bài giảng *",
                    value=ClassManagerState.new_lesson_title,
                    on_change=ClassManagerState.set_new_lesson_title,
                    width="100%",
                ),
                rx.input(
                    placeholder="File JSON * (vd: nihongo/a.json)",
                    value=ClassManagerState.new_lesson_file,
                    on_change=ClassManagerState.set_new_lesson_file,
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            "Thêm",
            ClassManagerState.confirm_add_lesson,
        ),
        _simple_modal(
            "Xóa lớp",
            ClassManagerState.show_delete_confirmation,
            ClassManagerState.close_delete_confirmation,
            rx.text(
                "Xóa lớp này, mọi lớp con và bài giảng bên trong?",
                color=T.TEXT_SECONDARY,
                font_size="0.9rem",
            ),
            "Xóa",
            ClassManagerState.confirm_delete_class,
        ),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("Quản lý lớp học", font_size="1rem", font_weight="700", color=T.TEXT_PRIMARY),
                    rx.text(
                        "Lớp chứa lớp con hoặc bài giảng (JSON)",
                        font_size="0.78rem",
                        color=T.TEXT_MUTED,
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.spacer(),
                rx.button(
                    "Gốc",
                    on_click=ClassManagerState.select_class(""),
                    bg=rx.cond(ClassManagerState.is_at_root, T.PRIMARY, T.BORDER_LIGHT),
                    color=rx.cond(ClassManagerState.is_at_root, "white", T.TEXT_PRIMARY),
                    border_radius=T.RADIUS_MD,
                    size="2",
                ),
                width="100%",
                align="center",
            ),
            rx.box(
                rx.text("Đang chọn", font_size="0.72rem", color=T.TEXT_MUTED),
                rx.text(ClassManagerState.breadcrumb, font_size="0.9rem", font_weight="600", color=T.TEXT_PRIMARY),
                rx.text(ClassManagerState.class_summary, font_size="0.78rem", color=T.TEXT_SECONDARY),
                width="100%",
                padding="0.65rem 0.85rem",
                bg=T.BORDER_LIGHT,
                border_radius=T.RADIUS_MD,
            ),
            rx.cond(
                ClassManagerState.message != "",
                rx.box(
                    rx.hstack(
                        rx.text(ClassManagerState.message, font_size="0.85rem", flex="1"),
                        rx.button(
                            rx.icon("x", size=14),
                            on_click=ClassManagerState.clear_message,
                            bg="transparent",
                            padding="0",
                        ),
                        width="100%",
                    ),
                    width="100%",
                    padding="0.6rem 0.85rem",
                    border_radius=T.RADIUS_MD,
                    bg=rx.cond(
                        ClassManagerState.message_type == "error",
                        T.DANGER_BG,
                        T.SUCCESS_BG,
                    ),
                ),
                rx.box(),
            ),
            rx.grid(
                _action_btn("folder-plus", "Thêm lớp con", ClassManagerState.open_add_subclass_dialog),
                _action_btn("pencil", "Đổi tên", ClassManagerState.open_rename_dialog),
                _action_btn("book-plus", "Bài giảng", ClassManagerState.open_add_lesson_dialog),
                _action_btn("trash-2", "Xóa", ClassManagerState.open_delete_confirmation, danger=True),
                grid_template_columns="repeat(2, 1fr)",
                gap="2",
                width="100%",
            ),
            rx.cond(
                ClassManagerState.is_at_root == False,
                rx.vstack(
                    rx.text("Bài giảng (class_lessons.json)", font_size="0.85rem", font_weight="600", color=T.TEXT_PRIMARY),
                    rx.cond(
                        ClassManagerState.class_lessons.length() > 0,
                        rx.vstack(
                            rx.foreach(ClassManagerState.class_lessons, _lesson_row),
                            spacing="2",
                            width="100%",
                        ),
                        rx.text(
                            "Chưa có bài giảng. Nhấn «Bài giảng» để thêm.",
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
                    ClassManagerState.tree_rows.length() > 0,
                    rx.vstack(
                        rx.foreach(ClassManagerState.tree_rows, _tree_row),
                        spacing="1",
                        width="100%",
                    ),
                    rx.text(
                        "Chưa có lớp. Chọn «Gốc» rồi nhấn «Thêm lớp con».",
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
        on_mount=ClassManagerState.load_current_class,
    )
