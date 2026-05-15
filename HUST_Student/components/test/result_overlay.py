import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_state import FolderState


def answer_record_row(record):
    return rx.box(
        rx.hstack(
            rx.cond(
                record.is_correct,
                rx.box(
                    rx.icon("check", size=16, color=T.SUCCESS),
                    bg=T.SUCCESS_BG,
                    border_radius="999px",
                    padding="0.3rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
                rx.box(
                    rx.icon("x", size=16, color=T.DANGER),
                    bg=T.DANGER_BG,
                    border_radius="999px",
                    padding="0.3rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
            ),
            rx.vstack(
                rx.text(record.question, font_size="0.85rem", color=T.TEXT_SECONDARY),
                rx.text(record.correct, font_size="1rem", font_weight="600", color=T.TEXT_PRIMARY),
                rx.cond(
                    ~record.is_correct,
                    rx.hstack(
                        rx.text("Bạn chọn: ", font_size="0.82rem", color=T.TEXT_MUTED),
                        rx.text(
                            record.chosen,
                            font_size="0.82rem",
                            color=T.DANGER,
                            font_weight="600",
                        ),
                        spacing="1",
                        align="center",
                    ),
                    rx.box(),
                ),
                spacing="1",
                align="start",
                flex="1",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="1rem 1.2rem",
        border_radius=T.RADIUS_MD,
        border=rx.cond(
            record.is_correct,
            f"1px solid {T.SUCCESS}",
            f"1px solid {T.DANGER}",
        ),
        bg=rx.cond(record.is_correct, T.SUCCESS_BG, T.DANGER_BG),
        width="100%",
    )


def result_overlay():
    total = FolderState.score_correct + FolderState.score_wrong
    pct = rx.cond(total > 0, (FolderState.score_correct * 100) // total, 0)

    return rx.cond(
        FolderState.show_result,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                rx.cond(FolderState.selected_set, FolderState.selected_set.title, "Kết quả"),
                                font_size="1.35rem",
                                font_weight="800",
                                color=T.TEXT_PRIMARY,
                            ),
                            rx.text("Hoàn thành bài kiểm tra", color=T.TEXT_SECONDARY, font_size="0.9rem"),
                            spacing="1",
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_test),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.vstack(
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        pct,
                                        "%",
                                        font_size="1.8rem",
                                        font_weight="700",
                                        color=rx.cond(pct >= 70, T.SUCCESS, T.DANGER),
                                    ),
                                    spacing="0",
                                    align="center",
                                ),
                                width="100px",
                                height="100px",
                                border_radius="999px",
                                border=rx.cond(
                                    pct >= 70,
                                    f"6px solid {T.SUCCESS}",
                                    f"6px solid {T.DANGER}",
                                ),
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                            rx.text(
                                rx.cond(pct >= 70, "Tốt lắm! 🎉", "Cố lên! 💪"),
                                font_size="0.85rem",
                                color=T.TEXT_SECONDARY,
                                text_align="center",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.vstack(
                            rx.hstack(
                                rx.box(width="12px", height="12px", border_radius="999px", bg=T.SUCCESS),
                                rx.text("Đúng", font_weight="600", flex="1", color=T.TEXT_PRIMARY),
                                rx.box(
                                    rx.text(
                                        FolderState.score_correct,
                                        color=T.SUCCESS,
                                        font_weight="700",
                                        font_size="1.1rem",
                                    ),
                                    bg=T.SUCCESS_BG,
                                    border_radius="8px",
                                    padding="0.2rem 0.8rem",
                                ),
                                spacing="3",
                                align="center",
                                width="200px",
                            ),
                            rx.hstack(
                                rx.box(width="12px", height="12px", border_radius="999px", bg=T.DANGER),
                                rx.text("Sai", font_weight="600", flex="1", color=T.TEXT_PRIMARY),
                                rx.box(
                                    rx.text(
                                        FolderState.score_wrong,
                                        color=T.DANGER,
                                        font_weight="700",
                                        font_size="1.1rem",
                                    ),
                                    bg=T.DANGER_BG,
                                    border_radius="8px",
                                    padding="0.2rem 0.8rem",
                                ),
                                spacing="3",
                                align="center",
                                width="200px",
                            ),
                            spacing="3",
                            align="start",
                            flex="1",
                        ),
                        rx.vstack(
                            rx.button(
                                rx.icon("refresh-cw", size=14),
                                " Làm lại tất cả",
                                on_click=FolderState.retry_all,
                                bg=T.PRIMARY,
                                color="white",
                                font_weight="700",
                                border_radius=T.RADIUS_SM,
                                width="100%",
                                _hover={"bg": T.PRIMARY_HOVER},
                            ),
                            rx.button(
                                rx.icon("x-circle", size=14),
                                " Luyện câu sai",
                                on_click=FolderState.retry_wrong_only,
                                bg=T.SURFACE,
                                color=T.DANGER,
                                font_weight="600",
                                border=f"1px solid {T.DANGER}",
                                border_radius=T.RADIUS_SM,
                                width="100%",
                                _hover={"bg": T.DANGER_BG},
                            ),
                            spacing="2",
                            width="140px",
                        ),
                        spacing="6",
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.text("Đáp án của bạn", font_weight="700", font_size="1rem", color=T.TEXT_PRIMARY),
                        rx.spacer(),
                        rx.hstack(
                            rx.button(
                                "Tất cả",
                                on_click=FolderState.set_show_wrong_only(False),
                                bg=rx.cond(~FolderState.show_wrong_only, T.PRIMARY, T.BORDER_LIGHT),
                                color=rx.cond(~FolderState.show_wrong_only, "white", T.TEXT_PRIMARY),
                                border_radius="8px",
                                size="2",
                                padding="0.3rem 0.8rem",
                                font_weight="600",
                            ),
                            rx.button(
                                "Câu sai",
                                on_click=FolderState.set_show_wrong_only(True),
                                bg=rx.cond(FolderState.show_wrong_only, T.DANGER, T.BORDER_LIGHT),
                                color=rx.cond(FolderState.show_wrong_only, "white", T.TEXT_PRIMARY),
                                border_radius="8px",
                                size="2",
                                padding="0.3rem 0.8rem",
                                font_weight="600",
                            ),
                            spacing="2",
                        ),
                        width="100%",
                        align="center",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                FolderState.answer_records,
                                lambda record: rx.cond(
                                    FolderState.show_wrong_only & record.is_correct,
                                    rx.box(),
                                    answer_record_row(record),
                                ),
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        max_height="320px",
                        overflow_y="auto",
                        width="100%",
                        padding_right="4px",
                    ),
                    spacing="5",
                    padding="1.8rem 2rem 2rem",
                    width="100%",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="620px",
                max_width="min(620px, calc(100vw - 2.5rem))",
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
