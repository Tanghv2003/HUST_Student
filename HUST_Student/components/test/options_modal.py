import reflex as rx

from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_state import FolderState


def test_option_button(label: str, mode: str):
    return rx.button(
        label,
        on_click=lambda: FolderState.set_test_mode(mode),
        width="100%",
        padding="1rem",
        border_radius="999px",
        border="1px solid #E5E7EB",
        bg=rx.cond(FolderState.test_mode == mode, "#4F46E5", "#F8FAFC"),
        color=rx.cond(FolderState.test_mode == mode, "white", "#111827"),
        _hover={"bg": "#E5F2FF"},
    )


def test_options_modal():
    return rx.cond(
        FolderState.show_test_options,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(FolderState.selected_set.title, font_size="1.5rem", font_weight="700"),
                            rx.text("Thiết lập bài kiểm tra", color="#6B7280", font_size="0.95rem"),
                            spacing="1", align="start",
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_test_options),
                        width="100%", align="center",
                    ),
                    rx.divider(),
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.text("Số câu hỏi", font_weight="600"),
                                rx.text(
                                    rx.cond(FolderState.selected_set, FolderState.selected_set.terms, 0),
                                    " câu", color="#111827",
                                ),
                            ),
                            rx.vstack(
                                rx.text("Tối đa", font_weight="600"),
                                rx.text(
                                    rx.cond(FolderState.selected_set, FolderState.selected_set.terms, 0),
                                    " câu", color="#6B7280",
                                ),
                            ),
                            rx.vstack(
                                rx.text("Trả lời bằng", font_weight="600"),
                                rx.select(
                                    ["Cả hai", "Native", "Foreign"],
                                    value=FolderState.answer_language,
                                    on_change=FolderState.set_answer_language,
                                    width="160px",
                                    border="1px solid #E5E7EB",
                                    border_radius="14px",
                                    padding="0.9rem 1rem",
                                ),
                            ),
                            spacing="8", width="100%",
                        ),
                        rx.text("Loại câu hỏi", font_weight="600"),
                        rx.grid(
                            test_option_button("Đúng/Sai", "dung_sai"),
                            test_option_button("Trắc nghiệm", "trac_nghiem"),
                            test_option_button("Ghép thẻ", "ghep_the"),
                            test_option_button("Tự luận", "tu_luan"),
                            template_columns="repeat(2, minmax(0, 1fr))",
                            gap="4", width="100%",
                        ),
                        rx.button(
                            "Bắt đầu làm kiểm tra",
                            on_click=FolderState.start_test,
                            bg="#4F46E5", color="white", border_radius="999px",
                            padding="1rem 1.5rem", _hover={"bg": "#4338CA"}, width="100%",
                        ),
                        spacing="4", width="100%",
                    ),
                    spacing="6", padding="2rem", width="100%",
                ),
                bg="white", border_radius="24px", width="560px", max_width="95%",
                box_shadow="0 20px 60px rgba(0,0,0,0.12)",
                on_click=rx.stop_propagation,
            ),
            position="fixed", top="0", left="0", right="0", bottom="0",
            display="flex", align_items="center", justify_content="center",
            bg="rgba(0,0,0,0.35)", z_index="999", padding="1.5rem",
            on_click=FolderState.close_test_options,
        ),
        rx.box(),
    )
