import reflex as rx

from HUST_Student.components.sidebar import sidebar
from HUST_Student.components.topbar import topbar
from HUST_Student.components.ui import theme as T

from HUST_Student.pages.library import library_page
from HUST_Student.pages.classes import classes_page
from HUST_Student.pages.folder_detail import folder_detail_page
from HUST_Student.pages.conversation import conversation_page
from HUST_Student.pages.roadmap import roadmap_page

from HUST_Student.states.navigation_state import NavigationState
from HUST_Student.services.studyset_service import load_studysets_raw
from HUST_Student.services.class_service import load_classes


class HomeState(rx.State):
    studyset_count: int = 0
    class_count: int = 0

    def load_counts(self):
        try:
            raw = load_studysets_raw()
            self.studyset_count = sum(len(v) for v in raw.values())
        except Exception:
            self.studyset_count = 0
        try:
            classes = load_classes()
            self.class_count = len(classes)
        except Exception:
            self.class_count = 0


def _kanji_card():
    return rx.box(
        rx.vstack(
            rx.text(
                "KANJI MỖI NGÀY",
                font_size="0.65rem", font_weight="700",
                color=T.TEXT_MUTED, letter_spacing="0.15em",
            ),
            rx.box(
                rx.text(
                    "志",
                    font_size="7rem", font_weight="400",
                    color=T.TEXT_PRIMARY, line_height="1",
                    font_family="'Noto Serif JP', 'Hiragino Mincho ProN', serif",
                ),
                padding="1.5rem 2rem", width="100%",
                display="flex", align_items="center", justify_content="center",
            ),
            rx.box(
                rx.vstack(
                    rx.text("CHÍ", font_size="1rem", font_weight="700",
                            color=T.TEXT_PRIMARY, letter_spacing="0.12em"),
                    rx.text("Ý chí, quyết tâm.", font_size="0.82rem",
                            color=T.TEXT_SECONDARY),
                    spacing="1", align="center",
                ),
                width="100%", padding="0.9rem 1rem",
                bg=T.SURFACE, border_top=f"1px solid {T.BORDER_LIGHT}",
                text_align="center",
            ),
            spacing="0", align="center", width="100%",
        ),
        bg=T.PAGE_BG, border_radius="20px",
        border=f"1px solid {T.BORDER}", overflow="hidden",
        width="240px", flex_shrink="0", box_shadow=T.SHADOW_CARD,
    )


def _hero_section():
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.vstack(
                    rx.text(
                        "Nơi nào có ý chí",
                        font_size="2.6rem", font_weight="800",
                        color=T.TEXT_PRIMARY, letter_spacing="-0.03em",
                        line_height="1.15",
                        font_family="'Playfair Display', 'Georgia', serif",
                    ),
                    rx.text(
                        "nơi đó có con đường",
                        font_size="2.6rem", font_weight="400",
                        font_style="italic", color=T.TEXT_SECONDARY,
                        letter_spacing="-0.01em", line_height="1.15",
                        font_family="'Playfair Display', 'Georgia', serif",
                    ),
                    spacing="0",
                ),
                rx.text(
                    "日本語を勉強しましょう。",
                    font_size="0.9rem", color=T.TEXT_MUTED,
                    letter_spacing="0.04em",
                ),
                rx.button(
                    rx.hstack(
                        rx.text("Bắt đầu học", font_size="0.9rem", font_weight="600"),
                        rx.icon("chevron-right", size=15),
                        spacing="1", align="center",
                    ),
                    on_click=NavigationState.go_library,
                    bg=T.TEXT_PRIMARY, color=T.SURFACE,
                    border_radius="999px", padding="0.7rem 1.5rem",
                    _hover={"opacity": "0.85"}, cursor="pointer", border="none",
                ),
                spacing="5", align="start", flex="1",
            ),
            _kanji_card(),
            width="100%", align="center", spacing="8",
        ),
        width="100%", padding="2rem 0 1.5rem",
        border_bottom=f"1px solid {T.BORDER_LIGHT}", margin_bottom="0.5rem",
    )


def _stat_card(icon: str, icon_color: str, label: str, value, on_click=None):
    is_clickable = on_click is not None
    return rx.box(
        rx.vstack(
            rx.icon(icon, size=24, color=icon_color),
            rx.text(label, font_size="0.8rem", color=T.TEXT_SECONDARY,
                    font_weight="500"),
            rx.text(value, font_size="1.5rem", font_weight="800",
                    color=T.TEXT_PRIMARY),
            spacing="2", align="center",
        ),
        bg=T.SURFACE, border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG, padding="1.25rem",
        flex="1", text_align="center", box_shadow=T.SHADOW_CARD,
        cursor="pointer" if is_clickable else "default",
        on_click=on_click,
        transition="all 0.12s ease",
        _hover={
            "box_shadow": T.SHADOW_CARD_HOVER,
            "border_color": icon_color if is_clickable else T.BORDER,
            "transform": "translateY(-1px)" if is_clickable else "none",
        },
    )


def homepage_content():
    return rx.vstack(
        _hero_section(),
        rx.hstack(
            _stat_card("book", T.PRIMARY, "Học phần",
                       HomeState.studyset_count,
                       on_click=NavigationState.go_library),
            _stat_card("graduation-cap", T.SUCCESS, "Lớp học",
                       HomeState.class_count,
                       on_click=NavigationState.go_classes),
            _stat_card("map", T.WARN, "Lộ trình",
                       "Xem ngay",
                       on_click=NavigationState.go_roadmap),
            spacing="4", width="100%",
        ),
        spacing="6", width="100%", align="start",
        on_mount=HomeState.load_counts,
    )


def content_router():
    return rx.cond(
        NavigationState.current_page == "home",
        homepage_content(),
        rx.cond(
            NavigationState.current_page == "library",
            library_page(),
            rx.cond(
                NavigationState.current_page == "folder_detail",
                folder_detail_page(),
                rx.cond(
                    NavigationState.current_page == "conversation",
                    conversation_page(),
                    rx.cond(
                        NavigationState.current_page == "roadmap",
                        roadmap_page(),
                        classes_page(),
                    ),
                ),
            ),
        ),
    )


def home():
    return rx.box(
        sidebar(),
        rx.box(
            rx.vstack(
                topbar(),
                rx.box(
                    content_router(),
                    flex="1", width="100%",
                    overflow_y="auto", padding_top="0.25rem",
                ),
                spacing="0", width="100%", height="100%", gap="0",
            ),
            margin_left="260px", padding="1.5rem 2rem 1rem",
            bg=T.PAGE_BG, height="100vh", overflow="hidden",
            display="flex", flex_direction="column",
        ),
        position="relative", width="100%", min_height="100vh",
    )