import reflex as rx

from HUST_Student.states.folder_state import FolderState
from HUST_Student.states.navigation_state import NavigationState


def option_button(icon: str, label: str, on_click=None):
    """Create an option button for study set actions"""
    return rx.vstack(
        rx.icon(
            icon,
            size=32,
            color="#4F46E5",
        ),
        rx.text(
            label,
            font_size="0.9rem",
            font_weight="600",
            text_align="center",
        ),
        align="center",
        spacing="2",
        padding="1.5rem",
        border="1px solid #E5E7EB",
        border_radius="12px",
        bg="white",
        cursor="pointer",
        on_click=on_click,
        _hover={
            "bg": "#EEF2FF",
            "border_color": "#4F46E5",
        },
    )


def test_option_button(label: str, mode: str):
    return rx.button(
        label,
        on_click=lambda: FolderState.set_test_mode(mode),
        width="100%",
        padding="1rem",
        border_radius="999px",
        border="1px solid #E5E7EB",
        bg=rx.cond(
            FolderState.test_mode == mode,
            "#4F46E5",
            "#F8FAFC",
        ),
        color=rx.cond(
            FolderState.test_mode == mode,
            "white",
            "#111827",
        ),
        _hover={"bg": "#E5F2FF"},
    )


def answer_option_button(option: str):
    """Single answer button rendered via rx.foreach — uses FolderState vars directly."""
    is_selected = FolderState.selected_answer == option
    is_correct = FolderState.correct_answer == option
    has_answered = FolderState.selected_answer != ""

    # Background logic:
    # - Not answered yet → white
    # - Answered & this is correct → green
    # - Answered & this is selected but wrong → red
    # - Answered & not selected, not correct → white (faded)
    bg_color = rx.cond(
        has_answered,
        rx.cond(
            is_correct,
            "#DCFCE7",           # green for correct answer always shown
            rx.cond(
                is_selected,
                "#FECACA",       # red for wrong selected
                "white",
            ),
        ),
        "white",
    )

    border_color = rx.cond(
        has_answered,
        rx.cond(
            is_correct,
            "#16A34A",
            rx.cond(
                is_selected,
                "#DC2626",
                "#E5E7EB",
            ),
        ),
        rx.cond(
            is_selected,
            "#4F46E5",
            "#E5E7EB",
        ),
    )

    text_color = rx.cond(
        has_answered,
        rx.cond(
            is_correct,
            "#15803D",
            rx.cond(
                is_selected,
                "#B91C1C",
                "#9CA3AF",      # gray out wrong non-selected after answer
            ),
        ),
        "#111827",
    )

    return rx.box(
        rx.hstack(
            rx.text(
                option,
                font_size="1rem",
                font_weight=rx.cond(is_correct & has_answered, "700", "500"),
                color=text_color,
                flex="1",
            ),
            rx.cond(
                has_answered & is_correct,
                rx.icon("check", size=18, color="#16A34A"),
                rx.cond(
                    has_answered & is_selected & ~is_correct,
                    rx.icon("x", size=18, color="#DC2626"),
                    rx.box(),
                ),
            ),
            align="center",
            width="100%",
        ),
        width="100%",
        padding="1.1rem 1.25rem",
        border=rx.cond(
            has_answered & is_correct,
            "2px solid #16A34A",
            rx.cond(
                has_answered & is_selected & ~is_correct,
                "2px solid #DC2626",
                "1.5px solid #E5E7EB",
            ),
        ),
        border_radius="14px",
        bg=bg_color,
        cursor=rx.cond(has_answered, "default", "pointer"),
        on_click=lambda: FolderState.set_selected_answer(option),
        _hover=rx.cond(
            has_answered,
            {},
            {"bg": "#F5F3FF", "border_color": "#4F46E5"},
        ),
        transition="all 0.15s ease",
    )


def trac_nghiem_section():
    """Full multiple-choice section using rx.foreach on FolderState.current_options."""
    current_word = rx.cond(
        FolderState.selected_set,
        FolderState.selected_set.words[FolderState.current_test_index],
        None,
    )

    # answer_language == "Foreign"  → câu hỏi là native, đáp án là foreign (back),  đáp án là tiếng Việt (front)
    # answer_language == "Native"   → câu hỏi là foreign, đáp án là native (front), đáp án là tiếng Nhật (back)
    # answer_language == "Cả hai"      → giống "Native": câu hỏi là tiếng Việt, đáp án tiếng Nhật
    question_text = rx.cond(
        current_word,
        rx.cond(
            FolderState.answer_language == "Foreign",
            current_word.back,   # hỏi bằng tiếng Nhật
            current_word.front,  # hỏi bằng tiếng Việt (Tiếng Nhật hoặc Cả hai)
        ),
        "—",
    )

    question_label = rx.cond(
        FolderState.answer_language == "Foreign",
        "Native",        # câu hỏi là chữ native
        "Foreign",       # câu hỏi là nghĩa foreign
    )

    return rx.vstack(
        # Header: label + counter
        rx.hstack(
            rx.text(
                question_label,
                font_size="0.85rem",
                font_weight="600",
                color="#6B7280",
                text_transform="uppercase",
                letter_spacing="0.05em",
            ),
            rx.spacer(),
            rx.text(
                FolderState.current_test_index + 1,
                " / ",
                FolderState.test_question_count,
                font_weight="700",
                color="#6B7280",
                font_size="0.9rem",
            ),
            width="100%",
            align="center",
        ),

        # Progress bar
        rx.progress(
            value=rx.cond(
                FolderState.test_question_count > 0,
                ((FolderState.current_test_index + 1) * 100) // FolderState.test_question_count,
                0,
            ),
            max=100,
            width="100%",
            color_scheme="indigo",
            size="1",
        ),

        # Question card
        rx.box(
            rx.text(
                question_text,
                font_size="1.4rem",
                font_weight="600",
                color="#111827",
                text_align="left",
                line_height="1.4",
            ),
            padding="1.5rem",
            border="1px solid #E5E7EB",
            border_radius="16px",
            bg="#F8FAFC",
            width="100%",
            min_height="100px",
        ),

        # Answer label
        rx.text(
            "Chọn đáp án đúng",
            font_size="0.82rem",
            color="#6B7280",
            font_weight="500",
        ),

        # 4 answer options via foreach in 2x2 grid
        rx.grid(
            rx.foreach(
                FolderState.current_options,
                answer_option_button,
            ),
            template_columns="repeat(2, minmax(0, 1fr))",
            gap="3",
            width="100%",
        ),

        # "Bạn không biết?" link
        rx.text(
            "Bạn không biết?",
            color="#4F46E5",
            font_weight="600",
            font_size="0.9rem",
            cursor="pointer",
            align_self="center",
            on_click=lambda: FolderState.set_selected_answer(FolderState.correct_answer),
            _hover={"text_decoration": "underline"},
        ),

        # Nav buttons
        rx.hstack(
            rx.button(
                "Đóng",
                on_click=FolderState.close_test,
                bg="#F3F4F6",
                color="#374151",
                border_radius="12px",
                padding="0.6rem 1.2rem",
                _hover={"bg": "#E5E7EB"},
            ),
            rx.spacer(),
            rx.button(
                "Tiếp theo →",
                on_click=FolderState.next_test_question,
                bg=rx.cond(
                    FolderState.selected_answer != "",
                    "#4F46E5",
                    "#C7D2FE",
                ),
                color="white",
                border_radius="12px",
                padding="0.6rem 1.4rem",
                _hover={"bg": "#4338CA"},
                cursor=rx.cond(
                    FolderState.selected_answer != "",
                    "pointer",
                    "not-allowed",
                ),
            ),
            width="100%",
            align="center",
        ),

        spacing="4",
        width="100%",
    )


def test_run_modal():
    """Full-screen overlay for the active test."""
    mode_label = rx.cond(
        FolderState.test_mode == "dung_sai",
        "Đúng/Sai",
        rx.cond(
            FolderState.test_mode == "trac_nghiem",
            "Trắc nghiệm",
            rx.cond(
                FolderState.test_mode == "ghep_the",
                "Ghép thẻ",
                "Tự luận",
            ),
        ),
    )

    return rx.cond(
        FolderState.show_test,
        rx.box(
            rx.box(
                rx.vstack(
                    # Modal header
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                rx.cond(
                                    FolderState.selected_set,
                                    FolderState.selected_set.title,
                                    "Kiểm tra",
                                ),
                                font_size="1.3rem",
                                font_weight="700",
                            ),
                            rx.hstack(
                                rx.badge(
                                    mode_label,
                                    color_scheme="indigo",
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
                        rx.button(
                            rx.icon("x", size=18),
                            on_click=FolderState.close_test,
                            bg="transparent",
                            color="#6B7280",
                            border_radius="8px",
                            padding="0.4rem",
                            _hover={"bg": "#F3F4F6"},
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.divider(),

                    # Mode-specific content
                    rx.cond(
                        FolderState.test_mode == "trac_nghiem",
                        trac_nghiem_section(),
                        # Fallback for other modes (tu_luan, dung_sai, ghep_the)
                        rx.vstack(
                            rx.text(
                                "Chế độ này đang được phát triển.",
                                color="#6B7280",
                                text_align="center",
                            ),
                            rx.button(
                                "Đóng",
                                on_click=FolderState.close_test,
                                bg="#F3F4F6",
                            ),
                            spacing="4",
                            align="center",
                            padding_y="2rem",
                        ),
                    ),

                    spacing="5",
                    padding="1.8rem 2rem 2rem",
                    width="100%",
                ),
                bg="white",
                border_radius="24px",
                width="580px",
                max_width="95vw",
                box_shadow="0 20px 60px rgba(0,0,0,0.14)",
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
            bg="rgba(17,24,39,0.4)",
            z_index="999",
            padding="1.5rem",
            on_click=FolderState.close_test,
        ),
        rx.box(),
    )


def set_options_modal():
    """Modal showing study set options"""
    return rx.cond(
        FolderState.show_set_options,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            FolderState.selected_set.title,
                            font_size="1.5rem",
                            font_weight="700",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon("x", size=20),
                            on_click=FolderState.close_set_options,
                            bg="transparent",
                            _hover={"bg": "#F3F4F6"},
                        ),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    rx.grid(
                        option_button("bookmark", "Thẻ ghi nhớ", on_click=FolderState.start_flashcards),
                        option_button("book-open", "Học"),
                        option_button("clipboard-check", "Kiểm tra", on_click=FolderState.open_test_options),
                        option_button("grid-3x3", "Khối hợp"),
                        option_button("zap", "Blast"),
                        option_button("shuffle", "Ghép thẻ"),
                        columns="3",
                        spacing="4",
                        width="100%",
                    ),
                    spacing="6",
                    padding="2rem",
                    width="100%",
                ),
                bg="white",
                border_radius="24px",
                width="600px",
                max_width="90%",
                box_shadow="0 20px 60px rgba(0,0,0,0.12)",
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
            bg="rgba(0,0,0,0.35)",
            z_index="999",
            padding="1.5rem",
            on_click=FolderState.close_set_options,
        ),
        rx.box(),
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
                                font_size="1.5rem",
                                font_weight="700",
                            ),
                            rx.text(
                                "Thiết lập bài kiểm tra",
                                color="#6B7280",
                                font_size="0.95rem",
                            ),
                            spacing="1",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon("x", size=20),
                            on_click=FolderState.close_test_options,
                            bg="transparent",
                            _hover={"bg": "#F3F4F6"},
                        ),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.text("Số câu hỏi", font_weight="600"),
                                rx.text(
                                    rx.cond(
                                        FolderState.selected_set,
                                        FolderState.selected_set.terms,
                                        0,
                                    ),
                                    " câu",
                                    color="#111827",
                                ),
                            ),
                            rx.vstack(
                                rx.text("Tối đa", font_weight="600"),
                                rx.text(
                                    rx.cond(
                                        FolderState.selected_set,
                                        FolderState.selected_set.terms,
                                        0,
                                    ),
                                    " câu",
                                    color="#6B7280",
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
                            spacing="8",
                            width="100%",
                        ),
                        rx.text("Loại câu hỏi", font_weight="600"),
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
                            bg="#4F46E5",
                            color="white",
                            border_radius="999px",
                            padding="1rem 1.5rem",
                            _hover={"bg": "#4338CA"},
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    spacing="6",
                    padding="2rem",
                    width="100%",
                ),
                bg="white",
                border_radius="24px",
                width="560px",
                max_width="95%",
                box_shadow="0 20px 60px rgba(0,0,0,0.12)",
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
            bg="rgba(0,0,0,0.35)",
            z_index="999",
            padding="1.5rem",
            on_click=FolderState.close_test_options,
        ),
        rx.box(),
    )


def studyset_card(title, terms):
    return rx.box(
        rx.vstack(
            rx.text(
                title,
                font_size="1.3rem",
                font_weight="700",
            ),
            rx.text(
                f"{terms} thuật ngữ",
                color="#6B7280",
            ),
            align="start",
            spacing="1",
        ),
        padding="1.2rem",
        border="1px solid #E5E7EB",
        border_radius="16px",
        bg="white",
        width="100%",
        cursor="pointer",
        on_click=lambda: FolderState.select_set(title),
        _hover={
            "bg": "#F9FAFB",
            "border_color": "#4F46E5",
        },
    )


def flashcard_overlay():
    current_word = rx.cond(
        FolderState.selected_set,
        FolderState.selected_set.words[FolderState.current_word_index],
        None,
    )

    current_word_text = rx.cond(
        current_word,
        rx.cond(
            FolderState.is_flipped,
            current_word.back,
            current_word.front,
        ),
        "",
    )

    current_position = rx.cond(
        FolderState.selected_set,
        FolderState.current_word_index + 1,
        0,
    )

    total_words = rx.cond(
        FolderState.selected_set,
        FolderState.selected_set.words.length(),
        0,
    )

    return rx.cond(
        FolderState.show_flashcards,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.text(
                        rx.cond(
                            FolderState.selected_set,
                            FolderState.selected_set.title,
                            "Flashcards",
                        ),
                        font_size="1.5rem",
                        font_weight="700",
                    ),
                    rx.text(
                        "Nhấp vào thẻ để lật",
                        color="#6B7280",
                        font_size="0.95rem",
                    ),
                    rx.box(
                        rx.text(
                            current_word_text,
                            font_size="2rem",
                            font_weight="700",
                            text_align="center",
                            padding="2rem",
                        ),
                        margin_top="1.5rem",
                        border="1px solid #E5E7EB",
                        border_radius="24px",
                        bg="white",
                        width="100%",
                        on_click=[rx.stop_propagation, FolderState.flip_card],
                        cursor="pointer",
                        padding="2rem",
                        min_height="220px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                    rx.hstack(
                        rx.button(
                            "← Trước",
                            on_click=FolderState.prev_word,
                            width="140px",
                            bg="#FFFFFF",
                            color="#111827",
                            border="1px solid #E5E7EB",
                            border_radius="999px",
                            padding="0.9rem 1.2rem",
                            _hover={"bg": "#F3F4F6"},
                        ),
                        rx.text(
                            current_position,
                            " / ",
                            total_words,
                            font_weight="700",
                        ),
                        rx.button(
                            "Tiếp →",
                            on_click=FolderState.next_word,
                            width="140px",
                            bg="#FFFFFF",
                            color="#111827",
                            border="1px solid #E5E7EB",
                            border_radius="999px",
                            padding="0.9rem 1.2rem",
                            _hover={"bg": "#F3F4F6"},
                        ),
                        spacing="4",
                        justify="center",
                        align="center",
                        width="100%",
                    ),
                    rx.button(
                        "Đóng",
                        on_click=FolderState.close_flashcards,
                        bg="#F3F4F6",
                        _hover={"bg": "#E5E7EB"},
                    ),
                    spacing="4",
                    width="100%",
                ),
                bg="white",
                border_radius="24px",
                width="720px",
                max_width="97%",
                box_shadow="0 24px 80px rgba(0,0,0,0.16)",
                padding="2.5rem",
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
            bg="rgba(0,0,0,0.35)",
            z_index="999",
            padding="1.5rem",
            on_click=FolderState.close_flashcards,
        ),
        rx.box(),
    )


def answer_record_row(record):
    """Single row in the result review list."""
    return rx.box(
        rx.hstack(
            # Icon đúng/sai
            rx.cond(
                record.is_correct,
                rx.box(
                    rx.icon("check", size=16, color="#16A34A"),
                    bg="#DCFCE7",
                    border_radius="999px",
                    padding="0.3rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
                rx.box(
                    rx.icon("x", size=16, color="#DC2626"),
                    bg="#FEE2E2",
                    border_radius="999px",
                    padding="0.3rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
            ),
            rx.vstack(
                # Câu hỏi
                rx.text(
                    record.question,
                    font_size="0.85rem",
                    color="#6B7280",
                ),
                # Đáp án đúng
                rx.text(
                    record.correct,
                    font_size="1rem",
                    font_weight="600",
                    color="#111827",
                ),
                # Nếu sai → hiện đáp án user chọn
                rx.cond(
                    ~record.is_correct,
                    rx.hstack(
                        rx.text(
                            "Bạn chọn: ",
                            font_size="0.82rem",
                            color="#9CA3AF",
                        ),
                        rx.text(
                            record.chosen,
                            font_size="0.82rem",
                            color="#DC2626",
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
        border_radius="14px",
        border=rx.cond(
            record.is_correct,
            "1px solid #BBF7D0",
            "1px solid #FECACA",
        ),
        bg=rx.cond(
            record.is_correct,
            "#F0FDF4",
            "#FFF5F5",
        ),
        width="100%",
    )


def result_overlay():
    """Màn hình kết quả sau khi hoàn thành bài kiểm tra."""
    total = FolderState.score_correct + FolderState.score_wrong
    pct = rx.cond(
        total > 0,
        (FolderState.score_correct * 100) // total,
        0,
    )

    return rx.cond(
        FolderState.show_result,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                rx.cond(
                                    FolderState.selected_set,
                                    FolderState.selected_set.title,
                                    "Kết quả",
                                ),
                                font_size="1.3rem",
                                font_weight="700",
                            ),
                            rx.text(
                                "Hoàn thành bài kiểm tra",
                                color="#6B7280",
                                font_size="0.9rem",
                            ),
                            spacing="1",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon("x", size=18),
                            on_click=FolderState.close_test,
                            bg="transparent",
                            color="#6B7280",
                            _hover={"bg": "#F3F4F6"},
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.divider(),

                    # Score summary
                    rx.hstack(
                        # Donut-style score display
                        rx.vstack(
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        pct,
                                        "%",
                                        font_size="1.8rem",
                                        font_weight="700",
                                        color=rx.cond(pct >= 70, "#16A34A", "#DC2626"),
                                    ),
                                    spacing="0",
                                    align="center",
                                ),
                                width="100px",
                                height="100px",
                                border_radius="999px",
                                border=rx.cond(
                                    pct >= 70,
                                    "6px solid #16A34A",
                                    "6px solid #DC2626",
                                ),
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                            rx.text(
                                rx.cond(pct >= 70, "Tốt lắm! 🎉", "Cố lên! 💪"),
                                font_size="0.85rem",
                                color="#6B7280",
                                text_align="center",
                            ),
                            spacing="2",
                            align="center",
                        ),

                        # Đúng / Sai counts
                        rx.vstack(
                            rx.hstack(
                                rx.box(width="12px", height="12px", border_radius="999px", bg="#16A34A"),
                                rx.text("Đúng", font_weight="600", flex="1"),
                                rx.box(
                                    rx.text(
                                        FolderState.score_correct,
                                        color="#16A34A",
                                        font_weight="700",
                                        font_size="1.1rem",
                                    ),
                                    bg="#DCFCE7",
                                    border_radius="8px",
                                    padding="0.2rem 0.8rem",
                                ),
                                spacing="3",
                                align="center",
                                width="200px",
                            ),
                            rx.hstack(
                                rx.box(width="12px", height="12px", border_radius="999px", bg="#DC2626"),
                                rx.text("Sai", font_weight="600", flex="1"),
                                rx.box(
                                    rx.text(
                                        FolderState.score_wrong,
                                        color="#DC2626",
                                        font_weight="700",
                                        font_size="1.1rem",
                                    ),
                                    bg="#FEE2E2",
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

                        # Action buttons
                        rx.vstack(
                            rx.button(
                                rx.icon("refresh-cw", size=14),
                                " Làm lại tất cả",
                                on_click=FolderState.retry_all,
                                bg="#4F46E5",
                                color="white",
                                border_radius="10px",
                                width="100%",
                                _hover={"bg": "#4338CA"},
                            ),
                            rx.button(
                                rx.icon("x-circle", size=14),
                                " Luyện câu sai",
                                on_click=FolderState.retry_wrong_only,
                                bg="white",
                                color="#DC2626",
                                border="1px solid #FECACA",
                                border_radius="10px",
                                width="100%",
                                _hover={"bg": "#FFF5F5"},
                            ),
                            spacing="2",
                            width="140px",
                        ),

                        spacing="6",
                        width="100%",
                        align="center",
                    ),

                    rx.divider(),

                    # Filter toggle
                    rx.hstack(
                        rx.text("Đáp án của bạn", font_weight="700", font_size="1rem"),
                        rx.spacer(),
                        rx.hstack(
                            rx.button(
                                "Tất cả",
                                on_click=FolderState.set_show_wrong_only(False),
                                bg=rx.cond(~FolderState.show_wrong_only, "#4F46E5", "#F3F4F6"),
                                color=rx.cond(~FolderState.show_wrong_only, "white", "#374151"),
                                border_radius="8px",
                                size="2",
                                padding="0.3rem 0.8rem",
                            ),
                            rx.button(
                                "Câu sai",
                                on_click=FolderState.set_show_wrong_only(True),
                                bg=rx.cond(FolderState.show_wrong_only, "#DC2626", "#F3F4F6"),
                                color=rx.cond(FolderState.show_wrong_only, "white", "#374151"),
                                border_radius="8px",
                                size="2",
                                padding="0.3rem 0.8rem",
                            ),
                            spacing="2",
                        ),
                        width="100%",
                        align="center",
                    ),

                    # Answer list
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                FolderState.answer_records,
                                lambda record: rx.cond(
                                    FolderState.show_wrong_only & record.is_correct,
                                    rx.box(),  # ẩn câu đúng khi đang lọc câu sai
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
                bg="white",
                border_radius="24px",
                width="620px",
                max_width="95vw",
                max_height="90vh",
                overflow_y="auto",
                box_shadow="0 20px 60px rgba(0,0,0,0.14)",
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
            bg="rgba(17,24,39,0.4)",
            z_index="999",
            padding="1.5rem",
            on_click=FolderState.close_test,
        ),
        rx.box(),
    )


def folder_detail_page():
    return rx.vstack(
        set_options_modal(),
        test_options_modal(),
        test_run_modal(),
        result_overlay(),
        flashcard_overlay(),
        rx.text(
            NavigationState.current_folder,
            font_size="2.5rem",
            font_weight="700",
        ),
        rx.vstack(
            rx.foreach(
                FolderState.current_sets,
                lambda item: studyset_card(
                    item.title,
                    item.terms,
                ),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        spacing="6",
    )