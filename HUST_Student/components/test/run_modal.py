import reflex as rx

from HUST_Student.components.test.essay import essay_section
from HUST_Student.components.test.multiple_choice import trac_nghiem_section
from HUST_Student.components.test.true_false import true_false_section
from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_state import FolderState


def test_run_modal():
    mode_label = rx.cond(
        FolderState.test_mode == "dung_sai", "Đúng/Sai",
        rx.cond(FolderState.test_mode == "trac_nghiem", "Trắc nghiệm",
                rx.cond(FolderState.test_mode == "ghep_the", "Ghép thẻ", "Tự luận")),
    )

    return rx.cond(
        FolderState.show_test,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                rx.cond(FolderState.selected_set, FolderState.selected_set.title, "Kiểm tra"),
                                font_size="1.35rem",
                                font_weight="800",
                                color=T.TEXT_PRIMARY,
                            ),
                            rx.hstack(
                                rx.badge(
                                    mode_label,
                                    color_scheme="blue",
                                    variant="soft",
                                    size="1",
                                ),
                                rx.badge(
                                    FolderState.answer_language,
                                    color_scheme="gray",
                                    variant="soft",
                                    size="1",
                                ),
                                spacing="2",
                            ),
                            spacing="1",
                            align="start",
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_test),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    rx.cond(
                        FolderState.test_mode == "trac_nghiem",
                        trac_nghiem_section(),
                        rx.cond(
                            FolderState.test_mode == "dung_sai",
                            true_false_section(),
                            rx.cond(
                                FolderState.test_mode == "tu_luan",
                                essay_section(),
                                rx.vstack(
                                    rx.text(
                                        "Chế độ này đang được phát triển.",
                                        color=T.TEXT_SECONDARY,
                                        text_align="center",
                                    ),
                                    rx.button(
                                        "Đóng",
                                        on_click=FolderState.close_test,
                                        bg=T.BORDER_LIGHT,
                                        color=T.TEXT_PRIMARY,
                                        border_radius=T.RADIUS_MD,
                                    ),
                                    spacing="4",
                                    align="center",
                                    padding_y="2rem",
                                ),
                            ),
                        ),
                    ),
                    spacing="5",
                    padding="1.75rem 2rem 2rem",
                    width="100%",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="580px",
                max_width="min(580px, calc(100vw - 2.5rem))",
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
            on_click=FolderState.close_test,
        ),
        rx.box(),
    )
