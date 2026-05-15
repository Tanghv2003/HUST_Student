import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_state import FolderState


def test_option_button(label: str, mode: str):
    return rx.button(
        label,
        on_click=lambda: FolderState.set_test_mode(mode),
        width="100%",
        padding="1rem",
        border_radius=T.RADIUS_PILL,
        border=f"1px solid {T.BORDER}",
        font_weight="600",
        bg=rx.cond(FolderState.test_mode == mode, T.PRIMARY, T.SURFACE),
        color=rx.cond(FolderState.test_mode == mode, "white", T.TEXT_PRIMARY),
        _hover={"border_color": T.PRIMARY, "cursor": "pointer"},
    )


def test_options_modal():
    return rx.cond(
        FolderState.show_test_options,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                FolderState.selected_set.title,
                                font_size="1.4rem",
                                font_weight="800",
                                color=T.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Thiết lập bài kiểm tra",
                                color=T.TEXT_SECONDARY,
                                font_size="0.95rem",
                            ),
                            spacing="1",
                            align="start",
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_test_options),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.text("Số câu hỏi", font_weight="600", color=T.TEXT_PRIMARY),
                                rx.text(
                                    rx.cond(FolderState.selected_set, FolderState.selected_set.terms, 0),
                                    " câu",
                                    color=T.TEXT_PRIMARY,
                                ),
                            ),
                            rx.vstack(
                                rx.text("Tối đa", font_weight="600", color=T.TEXT_PRIMARY),
                                rx.text(
                                    rx.cond(FolderState.selected_set, FolderState.selected_set.terms, 0),
                                    " câu",
                                    color=T.TEXT_SECONDARY,
                                ),
                            ),
                            rx.vstack(
                                rx.text("Trả lời bằng", font_weight="600", color=T.TEXT_PRIMARY),
                                rx.select(
                                    ["Cả hai", "Native", "Foreign"],
                                    value=FolderState.answer_language,
                                    on_change=FolderState.set_answer_language,
                                    width="160px",
                                    border=f"1px solid {T.BORDER}",
                                    border_radius=T.RADIUS_MD,
                                    padding="0.9rem 1rem",
                                ),
                            ),
                            spacing="8",
                            width="100%",
                        ),
                        rx.text("Loại câu hỏi", font_weight="600", color=T.TEXT_PRIMARY),
                        rx.grid(
                            test_option_button("Đúng/Sai", "dung_sai"),
                            test_option_button("Trắc nghiệm", "trac_nghiem"),
                            test_option_button("Ghép thẻ", "ghep_the"),
                            test_option_button("Tự luận", "tu_luan"),
                            template_columns="repeat(2, minmax(0, 1fr))",
                            gap="4",
                            width="100%",
                        ),
                        rx.button(
                            "Bắt đầu làm kiểm tra",
                            on_click=FolderState.start_test,
                            bg=T.PRIMARY,
                            color="white",
                            font_weight="700",
                            border_radius=T.RADIUS_PILL,
                            padding="1rem 1.5rem",
                            width="100%",
                            _hover={"bg": T.PRIMARY_HOVER, "cursor": "pointer"},
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    spacing="6",
                    padding="2rem",
                    width="100%",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="560px",
                max_width="min(560px, calc(100vw - 2.5rem))",
                max_height=T.MODAL_CONTENT_MAX_HEIGHT,
                min_height="0",
                overflow_y="auto",
                overflow_x="hidden",
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
            on_click=FolderState.close_test_options,
        ),
        rx.box(),
    )
