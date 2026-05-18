import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.kanji_state import ClassesTabState, KanjiItem, KanjiState


# ─────────────────────────────────────────────────────────────────
# KANJI DETAIL OVERLAY
# ─────────────────────────────────────────────────────────────────

def kanji_detail_overlay():
    k = KanjiState.selected_kanji
    return rx.cond(
        KanjiState.show_detail,
        rx.box(
            rx.box(
                rx.vstack(
                    # Close button row
                    rx.hstack(
                        rx.spacer(),
                        rx.button(
                            rx.icon("x", size=18),
                            on_click=KanjiState.close_detail,
                            bg="transparent",
                            color=T.TEXT_SECONDARY,
                            border_radius=T.RADIUS_SM,
                            padding="0.4rem",
                            _hover={"bg": T.BORDER_LIGHT},
                        ),
                        width="100%",
                    ),

                    # Big kanji display
                    rx.box(
                        rx.text(
                            rx.cond(k, k.kanji, ""),
                            font_size="7rem",
                            font_weight="900",
                            color=T.TEXT_PRIMARY,
                            line_height="1",
                            font_family="'Noto Sans JP', 'Yu Gothic', serif",
                        ),
                        width="100%",
                        min_height="220px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        bg="linear-gradient(135deg, #F0F4FF 0%, #E8EDF8 100%)",
                        border_radius=T.RADIUS_XL,
                        border=f"2px solid {T.PRIMARY_LIGHT}",
                    ),

                    # Meaning
                    rx.text(
                        rx.cond(k, k.meaning, ""),
                        font_size="1.5rem",
                        font_weight="800",
                        color=T.TEXT_PRIMARY,
                        text_align="center",
                        letter_spacing="-0.02em",
                    ),

                    # Stroke count badge
                    rx.hstack(
                        rx.icon("pen-line", size=13, color=T.TEXT_MUTED),
                        rx.text(
                            rx.cond(k, k.strokes, 0),
                            " nét",
                            font_size="0.78rem",
                            color=T.TEXT_MUTED,
                            font_weight="600",
                        ),
                        spacing="1",
                        align="center",
                        bg=T.BORDER_LIGHT,
                        padding="0.25rem 0.75rem",
                        border_radius="999px",
                    ),

                    rx.divider(),

                    # Readings side by side
                    rx.grid(
                        # Onyomi
                        rx.vstack(
                            rx.hstack(
                                rx.box(
                                    rx.text("音", font_size="0.75rem", font_weight="800",
                                            color="#E07B39"),
                                    bg="#FFF3E8",
                                    border_radius="6px",
                                    padding="0.15rem 0.4rem",
                                ),
                                rx.text("Onyomi", font_size="0.72rem", font_weight="700",
                                        color=T.TEXT_MUTED, text_transform="uppercase",
                                        letter_spacing="0.06em"),
                                spacing="2", align="center",
                            ),
                            rx.box(
                                rx.text(
                                    rx.cond(k,
                                        rx.cond(k.onyomi != "", k.onyomi, "—"),
                                        "—"),
                                    font_size="1.2rem",
                                    font_weight="700",
                                    color="#E07B39",
                                    text_align="center",
                                    font_family="'Noto Sans JP', serif",
                                ),
                                width="100%",
                                padding="1rem",
                                bg="#FFF8F3",
                                border_radius=T.RADIUS_MD,
                                border="1.5px solid #FDDCBB",
                                text_align="center",
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),

                        # Kunyomi
                        rx.vstack(
                            rx.hstack(
                                rx.box(
                                    rx.text("訓", font_size="0.75rem", font_weight="800",
                                            color="#3B82F6"),
                                    bg="#EFF6FF",
                                    border_radius="6px",
                                    padding="0.15rem 0.4rem",
                                ),
                                rx.text("Kunyomi", font_size="0.72rem", font_weight="700",
                                        color=T.TEXT_MUTED, text_transform="uppercase",
                                        letter_spacing="0.06em"),
                                spacing="2", align="center",
                            ),
                            rx.box(
                                rx.text(
                                    rx.cond(k,
                                        rx.cond(k.kunyomi != "", k.kunyomi, "—"),
                                        "—"),
                                    font_size="1.2rem",
                                    font_weight="700",
                                    color="#3B82F6",
                                    text_align="center",
                                    font_family="'Noto Sans JP', serif",
                                ),
                                width="100%",
                                padding="1rem",
                                bg="#EFF6FF",
                                border_radius=T.RADIUS_MD,
                                border="1.5px solid #BFDBFE",
                                text_align="center",
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),

                        template_columns="repeat(2, minmax(0, 1fr))",
                        gap="4",
                        width="100%",
                    ),

                    # Start learning button
                    rx.button(
                        rx.hstack(
                            rx.icon("play", size=16),
                            rx.text("Bắt đầu học", font_weight="700"),
                            spacing="2", align="center",
                        ),
                        bg=T.PRIMARY,
                        color="white",
                        border_radius=T.RADIUS_PILL,
                        padding="0.85rem 2rem",
                        width="100%",
                        font_size="1rem",
                        _hover={"bg": T.PRIMARY_HOVER},
                        on_click=KanjiState.close_detail,
                    ),

                    spacing="5",
                    width="100%",
                    padding="1.5rem 2rem 2rem",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="480px",
                max_width="min(480px, calc(100vw - 2.5rem))",
                max_height=T.MODAL_CONTENT_MAX_HEIGHT,
                overflow_y="auto",
                border=f"1px solid {T.BORDER}",
                box_shadow=T.SHADOW_MODAL,
                on_click=rx.stop_propagation,
            ),
            position="fixed",
            top="0", left="0", right="0", bottom="0",
            display="flex",
            align_items="center",
            justify_content="center",
            bg=T.OVERLAY_SCRIM,
            z_index="1000",
            padding=T.MODAL_OVERLAY_PADDING,
            on_click=KanjiState.close_detail,
        ),
        rx.box(),
    )


# ─────────────────────────────────────────────────────────────────
# KANJI CARD
# ─────────────────────────────────────────────────────────────────

def kanji_card(item: KanjiItem):
    return rx.box(
        rx.vstack(
            rx.text(
                item.kanji,
                font_size="2.5rem",
                font_weight="900",
                color=T.TEXT_PRIMARY,
                line_height="1",
                font_family="'Noto Sans JP', 'Yu Gothic', serif",
            ),
            rx.text(
                item.meaning,
                font_size="0.7rem",
                color=T.TEXT_SECONDARY,
                font_weight="500",
                text_align="center",
                no_of_lines=2,
                line_height="1.3",
            ),
            spacing="2",
            align="center",
        ),
        padding="0.9rem 0.5rem",
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        bg=T.SURFACE,
        cursor="pointer",
        box_shadow=T.SHADOW_CARD,
        transition="all 0.14s ease",
        text_align="center",
        min_height="95px",
        display="flex",
        align_items="center",
        justify_content="center",
        on_click=lambda: KanjiState.select_kanji(item.kanji, item.lesson),
        _hover={
            "border_color": T.PRIMARY,
            "box_shadow": T.SHADOW_CARD_HOVER,
            "transform": "translateY(-2px)",
            "bg": T.PRIMARY_TINT,
        },
    )


# ─────────────────────────────────────────────────────────────────
# KANJI PAGE
# ─────────────────────────────────────────────────────────────────

def _lesson_chip(ln: int):
    active = KanjiState.current_lesson_filter == ln
    return rx.box(
        rx.text(
            "Bài ", ln,
            font_size="0.8rem",
            font_weight="700",
            color=rx.cond(active, "white", T.TEXT_SECONDARY),
        ),
        padding="0.35rem 0.9rem",
        border_radius="999px",
        bg=rx.cond(active, T.PRIMARY, T.BORDER_LIGHT),
        cursor="pointer",
        border=rx.cond(active, f"1.5px solid {T.PRIMARY}", f"1.5px solid {T.BORDER}"),
        on_click=lambda: KanjiState.set_lesson_filter(ln),
        flex_shrink="0",
        transition="all 0.12s ease",
        _hover={"border_color": T.PRIMARY},
    )


def kanji_page():
    return rx.vstack(
        kanji_detail_overlay(),

        # Header
        rx.hstack(
            rx.hstack(
                rx.text(
                    "漢字",
                    font_size="2.2rem",
                    font_weight="900",
                    color=T.PRIMARY,
                    font_family="'Noto Sans JP', serif",
                    line_height="1",
                ),
                rx.vstack(
                    rx.text("Kanji N5", font_size="1.1rem", font_weight="800",
                            color=T.TEXT_PRIMARY, letter_spacing="-0.01em"),
                    rx.text("Kanji cơ bản trình độ N5",
                            font_size="0.82rem", color=T.TEXT_SECONDARY),
                    spacing="0", align="start",
                ),
                spacing="3", align="center",
            ),
            rx.spacer(),
            rx.vstack(
                rx.text(
                    KanjiState.all_kanji.length(),
                    font_size="1.75rem",
                    font_weight="800",
                    color=T.PRIMARY,
                    line_height="1",
                ),
                rx.text("chữ", font_size="0.72rem", color=T.TEXT_MUTED, font_weight="600"),
                spacing="0",
                align="center",
                bg=T.PRIMARY_TINT,
                border_radius=T.RADIUS_MD,
                padding="0.6rem 1rem",
                border=f"1px solid {T.PRIMARY_LIGHT}",
            ),
            width="100%",
            align="center",
        ),

        # Lesson filter chips
        rx.hstack(
            # "Tất cả" chip
            rx.box(
                rx.text(
                    "Tất cả",
                    font_size="0.8rem",
                    font_weight="700",
                    color=rx.cond(
                        KanjiState.current_lesson_filter == 0,
                        "white", T.TEXT_SECONDARY,
                    ),
                ),
                padding="0.35rem 0.9rem",
                border_radius="999px",
                bg=rx.cond(
                    KanjiState.current_lesson_filter == 0,
                    T.PRIMARY, T.BORDER_LIGHT,
                ),
                cursor="pointer",
                border=rx.cond(
                    KanjiState.current_lesson_filter == 0,
                    f"1.5px solid {T.PRIMARY}",
                    f"1.5px solid {T.BORDER}",
                ),
                on_click=lambda: KanjiState.set_lesson_filter(0),
                flex_shrink="0",
                transition="all 0.12s ease",
                _hover={"border_color": T.PRIMARY},
            ),
            rx.foreach(KanjiState.lessons, _lesson_chip),
            spacing="2",
            overflow_x="auto",
            padding_y="0.25rem",
            width="100%",
        ),

        # Kanji grid — flat, filtered by lesson
        rx.cond(
            KanjiState.filtered_kanji.length() > 0,
            rx.box(
                rx.grid(
                    rx.foreach(KanjiState.filtered_kanji, kanji_card),
                    template_columns="repeat(auto-fill, minmax(88px, 1fr))",
                    gap="3",
                    width="100%",
                ),
                width="100%",
                padding="1.25rem",
                bg=T.SURFACE,
                border=f"1px solid {T.BORDER}",
                border_radius=T.RADIUS_LG,
                box_shadow=T.SHADOW_CARD,
            ),
            rx.box(
                rx.text("Đang tải dữ liệu Kanji...",
                        color=T.TEXT_MUTED, font_size="0.9rem"),
                padding="2rem",
                text_align="center",
                width="100%",
            ),
        ),

        spacing="4",
        width="100%",
        align="start",
        on_mount=KanjiState.load_kanji,
    )


# ─────────────────────────────────────────────────────────────────
# CLASS CARD
# ─────────────────────────────────────────────────────────────────

def class_card(title: str, students: str, color: str, icon: str = "users"):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(icon, size=16, color=color),
                    bg=color + "18",
                    border_radius=T.RADIUS_MD,
                    padding="0.5rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.spacer(),
                rx.box(
                    width="8px",
                    height="8px",
                    border_radius="999px",
                    bg=T.SUCCESS,
                    box_shadow=f"0 0 0 3px {T.SUCCESS}22",
                ),
                width="100%",
                align="center",
            ),
            rx.vstack(
                rx.text(title, font_weight="700", font_size="1rem",
                        color=T.TEXT_PRIMARY, no_of_lines=1),
                rx.text(students, color=T.TEXT_SECONDARY, font_size="0.82rem"),
                spacing="1",
                align="start",
            ),
            rx.hstack(
                rx.button(
                    "Vào lớp",
                    bg=color,
                    color="white",
                    font_weight="600",
                    font_size="0.8rem",
                    border_radius=T.RADIUS_MD,
                    padding_x="1rem",
                    height="32px",
                    _hover={"opacity": "0.88", "cursor": "pointer"},
                ),
                rx.spacer(),
                rx.icon("arrow-right", size=16, color=T.TEXT_MUTED),
                width="100%",
                align="center",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        bg=T.SURFACE,
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        padding="1.1rem 1.2rem",
        box_shadow=T.SHADOW_CARD,
        transition="all 0.12s ease",
        _hover={
            "box_shadow": T.SHADOW_CARD_HOVER,
            "border_color": color,
            "transform": "translateY(-1px)",
        },
        cursor="pointer",
    )


def classes_tab_content():
    return rx.vstack(
        rx.grid(
            class_card("Tiếng Nhật N5", "42 học viên", "#23B26D", "users"),
            class_card("Toeic 700+", "28 học viên", T.PRIMARY, "users"),
            class_card("Kanji N4", "35 học viên", "#E879F9", "users"),
            class_card("Ngữ pháp N3", "19 học viên", T.WARN, "users"),
            template_columns="repeat(2, minmax(0, 1fr))",
            gap="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
        align="start",
    )


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
        spacing="2",
        align="center",
        padding="0.55rem 1rem",
        border_radius=T.RADIUS_MD,
        bg=rx.cond(active, T.PRIMARY_TINT, "transparent"),
        border=rx.cond(active, f"1.5px solid {T.PRIMARY_LIGHT}",
                       "1.5px solid transparent"),
        cursor="pointer",
        transition="all 0.12s ease",
        on_click=on_click,
        _hover={"bg": T.PRIMARY_TINT},
        flex_shrink="0",
    )


# ─────────────────────────────────────────────────────────────────
# MAIN classes_page
# ─────────────────────────────────────────────────────────────────

def classes_page():
    return rx.vstack(
        # Header
        rx.hstack(
            rx.vstack(
                rx.text(
                    "Lớp học",
                    font_size="1.5rem",
                    font_weight="800",
                    color=T.TEXT_PRIMARY,
                    letter_spacing="-0.02em",
                ),
                rx.text(
                    "Tham gia lớp học và luyện tập Kanji",
                    font_size="0.85rem",
                    color=T.TEXT_SECONDARY,
                ),
                spacing="0",
                align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=15),
                    rx.text("Tạo lớp", font_size="0.875rem", font_weight="600"),
                    spacing="2",
                    align="center",
                ),
                bg=T.PRIMARY,
                color="white",
                border_radius=T.RADIUS_MD,
                padding_x="1rem",
                height="36px",
                _hover={"bg": T.PRIMARY_HOVER},
            ),
            width="100%",
            align="center",
        ),

        # Tab switcher
        rx.hstack(
            _tab(
                "Lớp học của tôi", "graduation-cap",
                ClassesTabState.active_tab == "lop_hoc",
                lambda: ClassesTabState.set_tab("lop_hoc"),
            ),
            _tab(
                "Kanji N5", "book-open",
                ClassesTabState.active_tab == "kanji",
                lambda: ClassesTabState.set_tab("kanji"),
            ),
            spacing="2",
            width="100%",
            overflow_x="auto",
            padding_bottom="0.25rem",
        ),

        rx.divider(),

        # Content
        rx.box(
            rx.cond(
                ClassesTabState.active_tab == "kanji",
                kanji_page(),
                classes_tab_content(),
            ),
            width="100%",
            flex="1",
            overflow_y="auto",
        ),

        spacing="4",
        width="100%",
        height="100%",
        align="start",
    )