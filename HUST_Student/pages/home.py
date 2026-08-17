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


# ---------------------------------------------------------------------------
# Kanji data  (char, reading_vi, meaning_vi, on_yomi, kun_yomi, level, theme)
# ---------------------------------------------------------------------------
KANJI_LIST = [
    # Quyết tâm / Ý chí
    ("志", "CHÍ",     "Ý chí, quyết tâm",   "シ",     "こころざ・す", "N3", "Quyết tâm"),
    ("勇", "DŨNG",    "Dũng cảm, can đảm",   "ユウ",   "いさ・む",   "N3", "Quyết tâm"),
    ("努", "NỖ",      "Cố gắng, nỗ lực",     "ド",     "つと・める", "N3", "Quyết tâm"),
    ("力", "LỰC",     "Sức mạnh, năng lực",  "リョク", "ちから",     "N5", "Quyết tâm"),
    ("強", "CƯỜNG",   "Mạnh mẽ, kiên cường", "キョウ", "つよ・い",   "N4", "Quyết tâm"),
    ("克", "KHẮC",    "Vượt qua, chinh phục","コク",   "か・つ",     "N2", "Quyết tâm"),
    # Công danh / Sự nghiệp
    ("功", "CÔNG",    "Công lao, thành tích","コウ",   "いさお",     "N3", "Công danh"),
    ("名", "DANH",    "Danh tiếng, tên tuổi","メイ",   "な",         "N4", "Công danh"),
    ("業", "NGHIỆP",  "Sự nghiệp, nghề nghiệp","ギョウ","わざ",      "N3", "Công danh"),
    ("栄", "VINH",    "Vinh quang, phồn thịnh","エイ", "さか・える", "N2", "Công danh"),
    ("誉", "DỰ",      "Danh dự, vinh dự",    "ヨ",     "ほま・れ",   "N2", "Công danh"),
    ("勝", "THẮNG",   "Chiến thắng, thắng lợi","ショウ","か・つ",    "N4", "Công danh"),
    # Tình yêu / Tình cảm
    ("愛", "ÁI",      "Tình yêu, yêu thương","アイ",   "いと・しい", "N3", "Tình yêu"),
    ("恋", "LUYẾN",   "Tình yêu lãng mạn",   "レン",   "こい",       "N3", "Tình yêu"),
    ("情", "TÌNH",    "Tình cảm, cảm xúc",   "ジョウ", "なさけ",     "N3", "Tình yêu"),
    ("慕", "MỘ",      "Nhớ nhung, ngưỡng mộ","ボ",     "した・う",   "N2", "Tình yêu"),
    ("縁", "DUYÊN",   "Duyên phận, cơ duyên","エン",   "えん",       "N2", "Tình yêu"),
    ("絆", "BẠCH",    "Sợi dây kết nối",     "ハン",   "きずな",     "N1", "Tình yêu"),
    # Ước mơ / Khát vọng
    ("夢", "MỘNG",    "Giấc mơ, ước mơ",     "ム",     "ゆめ",       "N3", "Ước mơ"),
    ("希", "HY",      "Hy vọng, mong muốn",  "キ",     "まれ",       "N3", "Ước mơ"),
    ("望", "VỌNG",    "Khao khát, mong đợi", "ボウ",   "のぞ・む",   "N3", "Ước mơ"),
    ("憧", "ĐỒNG",    "Ngưỡng mộ, ao ước",   "ショウ", "あこが・れる","N1","Ước mơ"),
    ("願", "NGUYỆN",  "Nguyện vọng, cầu mong","ガン",  "ねが・う",   "N3", "Ước mơ"),
    ("想", "TƯỞNG",   "Suy nghĩ, tưởng tượng","ソウ",  "おも・う",   "N3", "Ước mơ"),
    # Tâm hồn / Triết lý
    ("心", "TÂM",     "Trái tim, tâm hồn",   "シン",   "こころ",     "N4", "Tâm hồn"),
    ("道", "ĐẠO",     "Con đường, đạo lý",   "ドウ",   "みち",       "N4", "Tâm hồn"),
    ("徳", "ĐỨC",     "Đức hạnh, phẩm giá",  "トク",   "—",          "N2", "Tâm hồn"),
    ("義", "NGHĨA",   "Chính nghĩa, đạo nghĩa","ギ",   "よし",       "N2", "Tâm hồn"),
    ("誠", "THÀNH",   "Thành thật, chân thành","セイ",  "まこと",     "N2", "Tâm hồn"),
    ("和", "HÒA",     "Hòa bình, hòa hợp",   "ワ",     "やわ・らぐ", "N4", "Tâm hồn"),
]

THEMES = ["Tất cả", "Quyết tâm", "Công danh", "Tình yêu", "Ước mơ", "Tâm hồn"]

LEVEL_COLORS = {
    "N5": ("#e8f5e9", "#2e7d32"),
    "N4": ("#e3f2fd", "#1565c0"),
    "N3": ("#fff8e1", "#f57f17"),
    "N2": ("#fce4ec", "#c62828"),
    "N1": ("#ede7f6", "#4527a0"),
}


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
class HomeState(rx.State):
    selected_index: int = 0
    active_theme: str = "Tất cả"

    @rx.var
    def filtered_kanjis(self) -> list[dict]:
        result = []
        for i, (char, reading, meaning, on, kun, level, theme) in enumerate(KANJI_LIST):
            if self.active_theme == "Tất cả" or theme == self.active_theme:
                result.append({
                    "index": i,
                    "char": char,
                    "reading": reading,
                    "meaning": meaning,
                    "on": on,
                    "kun": kun,
                    "level": level,
                    "theme": theme,
                })
        return result

    @rx.var
    def current_kanji(self) -> dict:
        idx = self.selected_index
        if idx < 0 or idx >= len(KANJI_LIST):
            idx = 0
        char, reading, meaning, on, kun, level, theme = KANJI_LIST[idx]
        return {
            "char": char,
            "reading": reading,
            "meaning": meaning,
            "on": on,
            "kun": kun,
            "level": level,
            "theme": theme,
        }

    def select_kanji(self, index: int):
        self.selected_index = index

    def set_theme(self, theme: str):
        self.active_theme = theme
        # Select first kanji of new theme
        for i, row in enumerate(KANJI_LIST):
            if theme == "Tất cả" or row[6] == theme:
                self.selected_index = i
                break


# ---------------------------------------------------------------------------
# Level badge
# ---------------------------------------------------------------------------
def _level_badge(level: str):
    bg, color = LEVEL_COLORS.get(level, ("#f5f5f5", "#616161"))
    return rx.box(
        rx.text(level, font_size="0.55rem", font_weight="700",
                color=color, letter_spacing="0.05em"),
        bg=bg, border_radius="4px", padding="2px 6px",
    )


# ---------------------------------------------------------------------------
# Kanji grid item
# ---------------------------------------------------------------------------
def _kanji_grid_item(item: dict):
    return rx.box(
        rx.vstack(
            rx.text(
                item["char"],
                font_family="'Noto Serif JP','Hiragino Mincho ProN',serif",
                font_size="1.05rem", line_height="1",
                color=T.TEXT_PRIMARY,
            ),
            rx.text(
                item["reading"],
                font_size="0.45rem", color=T.TEXT_MUTED,
                letter_spacing="0.03em",
            ),
            spacing="1", align="center",
        ),
        padding="5px 2px",
        border_radius="8px",
        border=rx.cond(
            HomeState.selected_index == item["index"],
            f"1.5px solid {T.PRIMARY}",
            f"0.5px solid {T.BORDER_LIGHT}",
        ),
        bg=rx.cond(
            HomeState.selected_index == item["index"],
            T.SURFACE,
            "transparent",
        ),
        cursor="pointer",
        on_click=HomeState.select_kanji(item["index"]),
        transition="all 0.12s ease",
        _hover={"border_color": T.BORDER, "bg": T.SURFACE},
        width="100%",
    )


# ---------------------------------------------------------------------------
# Theme filter tabs
# ---------------------------------------------------------------------------
def _theme_tab(theme: str):
    return rx.box(
        rx.text(theme, font_size="0.6rem", font_weight="500",
                color=rx.cond(
                    HomeState.active_theme == theme,
                    T.TEXT_PRIMARY,
                    T.TEXT_MUTED,
                )),
        padding="3px 8px",
        border_radius="999px",
        bg=rx.cond(
            HomeState.active_theme == theme,
            T.SURFACE,
            "transparent",
        ),
        border=rx.cond(
            HomeState.active_theme == theme,
            f"0.5px solid {T.BORDER}",
            "0.5px solid transparent",
        ),
        cursor="pointer",
        on_click=HomeState.set_theme(theme),
        transition="all 0.12s ease",
        white_space="nowrap",
    )


# ---------------------------------------------------------------------------
# Main kanji card
# ---------------------------------------------------------------------------
def _kanji_card():
    return rx.box(
        # ── Header
        rx.hstack(
            rx.hstack(
                rx.box(
                    width="6px", height="6px", border_radius="50%",
                    bg=T.SUCCESS,
                ),
                rx.text("KANJI MỖI NGÀY", font_size="0.58rem", font_weight="700",
                        color=T.TEXT_MUTED, letter_spacing="0.12em"),
                spacing="2", align="center",
            ),
            _level_badge(HomeState.current_kanji["level"]),
            justify="between", align="center", width="100%",
            padding="0.6rem 0.9rem 0.5rem",
            border_bottom=f"1px solid {T.BORDER_LIGHT}",
        ),

        # ── Main display: big char + readings
        rx.hstack(
            rx.text(
                HomeState.current_kanji["char"],
                font_family="'Noto Serif JP','Hiragino Mincho ProN',serif",
                font_size="4.2rem", line_height="1",
                color=T.TEXT_PRIMARY, flex_shrink="0",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        HomeState.current_kanji["reading"],
                        font_size="1.05rem", font_weight="700",
                        color=T.TEXT_PRIMARY, letter_spacing="0.1em",
                    ),
                    rx.text(
                        HomeState.current_kanji["theme"],
                        font_size="0.58rem", color=T.TEXT_MUTED,
                        padding="2px 6px",
                        border=f"0.5px solid {T.BORDER_LIGHT}",
                        border_radius="999px",
                    ),
                    spacing="2", align="center",
                ),
                rx.text(
                    HomeState.current_kanji["meaning"],
                    font_size="0.75rem", color=T.TEXT_SECONDARY,
                ),
                rx.hstack(
                    rx.vstack(
                        rx.box(
                            rx.text(HomeState.current_kanji["on"],
                                    font_size="0.65rem", color=T.TEXT_SECONDARY),
                            border=f"0.5px solid {T.BORDER}",
                            border_radius="999px", padding="1px 8px",
                            bg=T.PAGE_BG,
                        ),
                        rx.text("On", font_size="0.55rem", color=T.TEXT_MUTED),
                        spacing="1", align="center",
                    ),
                    rx.vstack(
                        rx.box(
                            rx.text(HomeState.current_kanji["kun"],
                                    font_size="0.65rem", color=T.TEXT_SECONDARY),
                            border=f"0.5px solid {T.BORDER}",
                            border_radius="999px", padding="1px 8px",
                            bg=T.PAGE_BG,
                        ),
                        rx.text("Kun", font_size="0.55rem", color=T.TEXT_MUTED),
                        spacing="1", align="center",
                    ),
                    spacing="2",
                ),
                spacing="2", align="start",
            ),
            spacing="4", align="center",
            padding="0.85rem 0.9rem",
        ),

        # ── Theme filter tabs
        rx.box(
            rx.hstack(
                *[_theme_tab(t) for t in THEMES],
                spacing="1", overflow_x="auto",
            ),
            padding="0.4rem 0.9rem",
            border_top=f"0.5px solid {T.BORDER_LIGHT}",
            border_bottom=f"0.5px solid {T.BORDER_LIGHT}",
        ),

        # ── Kanji grid (filtered)
        rx.box(
            rx.text(
                "CÁC CHỮ LIÊN QUAN",
                font_size="0.5rem", color=T.TEXT_MUTED,
                letter_spacing="0.1em", margin_bottom="0.4rem",
            ),
            rx.grid(
                rx.foreach(HomeState.filtered_kanjis, _kanji_grid_item),
                columns="6", spacing="1", width="100%",
            ),
            padding="0.6rem 0.9rem 0.75rem",
            width="100%",
        ),

        # Card container
        bg=T.SURFACE,
        border=f"1px solid {T.BORDER}",
        border_radius="20px",
        overflow="hidden",
        width="290px",
        flex_shrink="0",
        box_shadow=T.SHADOW_CARD,
    )


# ---------------------------------------------------------------------------
# Hero section
# ---------------------------------------------------------------------------
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
                        font_family="'Playfair Display','Georgia',serif",
                    ),
                    rx.text(
                        "nơi đó có con đường",
                        font_size="2.6rem", font_weight="400",
                        font_style="italic", color=T.TEXT_SECONDARY,
                        letter_spacing="-0.01em", line_height="1.15",
                        font_family="'Playfair Display','Georgia',serif",
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
            width="100%", align="start", spacing="8",
        ),
        width="100%",
        padding="2rem 0 1.5rem",
        border_bottom=f"1px solid {T.BORDER_LIGHT}",
        margin_bottom="0.25rem",
    )


# ---------------------------------------------------------------------------
# Quick access bar
# ---------------------------------------------------------------------------
def _quick_access_btn(icon: str, label: str, on_click=None):
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=13, color=T.TEXT_MUTED),
            rx.text(label, font_size="0.75rem", color=T.TEXT_SECONDARY),
            spacing="1", align="center",
        ),
        padding="0.3rem 0.75rem",
        border_radius="999px",
        border=f"0.5px solid {T.BORDER}",
        bg=T.SURFACE,
        cursor="pointer",
        on_click=on_click,
        transition="all 0.12s ease",
        _hover={
            "border_color": T.TEXT_MUTED,
            "bg": T.PAGE_BG,
        },
    )


def _quick_access():
    return rx.hstack(
        rx.text("Truy cập nhanh:",
                font_size="0.73rem", color=T.TEXT_MUTED,
                white_space="nowrap", flex_shrink="0"),
        rx.hstack(
            _quick_access_btn("book", "Thư viện", on_click=NavigationState.go_library),
            _quick_access_btn("message-circle", "Hội thoại"),
            _quick_access_btn("map", "Lộ trình", on_click=NavigationState.go_roadmap),
            _quick_access_btn("graduation-cap", "Lớp học", on_click=NavigationState.go_classes),
            spacing="2", flex_wrap="wrap",
        ),
        spacing="3", align="center", width="100%",
    )


# ---------------------------------------------------------------------------
# Homepage content (adjusted to push quick access to bottom)
# ---------------------------------------------------------------------------
def homepage_content():
    return rx.box(
        # Hero section takes remaining space
        rx.box(
            _hero_section(),
            flex="1",
            width="100%",
        ),
        # Quick access always at bottom
        _quick_access(),
        display="flex",
        flex_direction="column",
        height="100%",
        width="100%",
        gap="5",
        flex="1",               # ensure this box fills parent
    )


# ---------------------------------------------------------------------------
# Content router
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Root page (with flex layout to fill height)
# ---------------------------------------------------------------------------
def home():
    return rx.box(
        sidebar(),
        rx.box(
            rx.vstack(
                topbar(),
                rx.box(
                    content_router(),
                    flex="1",
                    width="100%",
                    overflow_y="auto",
                    padding_top="0.25rem",
                    display="flex",          # enable flex for content
                    flex_direction="column", # column direction
                ),
                spacing="0",
                width="100%",
                height="100%",
                align="stretch",
            ),
            margin_left="260px",
            padding="1.5rem 2rem 1rem",
            bg=T.PAGE_BG,
            height="100vh",
            overflow="hidden",
            display="flex",
            flex_direction="column",
        ),
        position="relative",
        width="100%",
        min_height="100vh",
    )