import reflex as rx

from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_state import FolderState


def answer_record_row(record):
    return rx.box(
        rx.hstack(
            rx.cond(
                record.is_correct,
                rx.box(
                    rx.icon("check", size=16, color="#16A34A"),
                    bg="#DCFCE7", border_radius="999px", padding="0.3rem",
                    display="flex", align_items="center", justify_content="center", flex_shrink="0",
                ),
                rx.box(
                    rx.icon("x", size=16, color="#DC2626"),
                    bg="#FEE2E2", border_radius="999px", padding="0.3rem",
                    display="flex", align_items="center", justify_content="center", flex_shrink="0",
                ),
            ),
            rx.vstack(
                rx.text(record.question, font_size="0.85rem", color="#6B7280"),
                rx.text(record.correct, font_size="1rem", font_weight="600", color="#111827"),
                rx.cond(
                    ~record.is_correct,
                    rx.hstack(
                        rx.text("Bạn chọn: ", font_size="0.82rem", color="#9CA3AF"),
                        rx.text(record.chosen, font_size="0.82rem", color="#DC2626", font_weight="600"),
                        spacing="1", align="center",
                    ),
                    rx.box(),
                ),
                spacing="1", align="start", flex="1",
            ),
            spacing="3", align="start", width="100%",
        ),
        padding="1rem 1.2rem",
        border_radius="14px",
        border=rx.cond(record.is_correct, "1px solid #BBF7D0", "1px solid #FECACA"),
        bg=rx.cond(record.is_correct, "#F0FDF4", "#FFF5F5"),
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
                                font_size="1.3rem", font_weight="700",
                            ),
                            rx.text("Hoàn thành bài kiểm tra", color="#6B7280", font_size="0.9rem"),
                            spacing="1",
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_test),
                        width="100%", align="center",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.vstack(
                            rx.box(
                                rx.vstack(
                                    rx.text(pct, "%", font_size="1.8rem", font_weight="700",
                                            color=rx.cond(pct >= 70, "#16A34A", "#DC2626")),
                                    spacing="0", align="center",
                                ),
                                width="100px", height="100px", border_radius="999px",
                                border=rx.cond(pct >= 70, "6px solid #16A34A", "6px solid #DC2626"),
                                display="flex", align_items="center", justify_content="center",
                            ),
                            rx.text(rx.cond(pct >= 70, "Tốt lắm! 🎉", "Cố lên! 💪"),
                                    font_size="0.85rem", color="#6B7280", text_align="center"),
                            spacing="2", align="center",
                        ),
                        rx.vstack(
                            rx.hstack(
                                rx.box(width="12px", height="12px", border_radius="999px", bg="#16A34A"),
                                rx.text("Đúng", font_weight="600", flex="1"),
                                rx.box(
                                    rx.text(FolderState.score_correct, color="#16A34A", font_weight="700", font_size="1.1rem"),
                                    bg="#DCFCE7", border_radius="8px", padding="0.2rem 0.8rem",
                                ),
                                spacing="3", align="center", width="200px",
                            ),
                            rx.hstack(
                                rx.box(width="12px", height="12px", border_radius="999px", bg="#DC2626"),
                                rx.text("Sai", font_weight="600", flex="1"),
                                rx.box(
                                    rx.text(FolderState.score_wrong, color="#DC2626", font_weight="700", font_size="1.1rem"),
                                    bg="#FEE2E2", border_radius="8px", padding="0.2rem 0.8rem",
                                ),
                                spacing="3", align="center", width="200px",
                            ),
                            spacing="3", align="start", flex="1",
                        ),
                        rx.vstack(
                            rx.button(
                                rx.icon("refresh-cw", size=14), " Làm lại tất cả",
                                on_click=FolderState.retry_all,
                                bg="#4F46E5", color="white", border_radius="10px",
                                width="100%", _hover={"bg": "#4338CA"},
                            ),
                            rx.button(
                                rx.icon("x-circle", size=14), " Luyện câu sai",
                                on_click=FolderState.retry_wrong_only,
                                bg="white", color="#DC2626",
                                border="1px solid #FECACA", border_radius="10px",
                                width="100%", _hover={"bg": "#FFF5F5"},
                            ),
                            spacing="2", width="140px",
                        ),
                        spacing="6", width="100%", align="center",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.text("Đáp án của bạn", font_weight="700", font_size="1rem"),
                        rx.spacer(),
                        rx.hstack(
                            rx.button(
                                "Tất cả",
                                on_click=FolderState.set_show_wrong_only(False),
                                bg=rx.cond(~FolderState.show_wrong_only, "#4F46E5", "#F3F4F6"),
                                color=rx.cond(~FolderState.show_wrong_only, "white", "#374151"),
                                border_radius="8px", size="2", padding="0.3rem 0.8rem",
                            ),
                            rx.button(
                                "Câu sai",
                                on_click=FolderState.set_show_wrong_only(True),
                                bg=rx.cond(FolderState.show_wrong_only, "#DC2626", "#F3F4F6"),
                                color=rx.cond(FolderState.show_wrong_only, "white", "#374151"),
                                border_radius="8px", size="2", padding="0.3rem 0.8rem",
                            ),
                            spacing="2",
                        ),
                        width="100%", align="center",
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
                            spacing="2", width="100%",
                        ),
                        max_height="320px", overflow_y="auto", width="100%", padding_right="4px",
                    ),
                    spacing="5", padding="1.8rem 2rem 2rem", width="100%",
                ),
                bg="white", border_radius="24px", width="620px", max_width="95vw",
                max_height="90vh", overflow_y="auto",
                box_shadow="0 20px 60px rgba(0,0,0,0.14)",
                on_click=rx.stop_propagation,
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg="rgba(17,24,39,0.4)", z_index="999", padding="1.5rem",
            on_click=FolderState.close_test,
        ),
        rx.box(),
    )
