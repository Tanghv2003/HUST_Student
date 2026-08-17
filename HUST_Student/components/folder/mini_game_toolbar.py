import reflex as rx

from HUST_Student.components.folder.mini_i18n import mini_txt
from HUST_Student.components.ui import theme as T
from HUST_Student.states.folder_state import FolderState


def mini_settings_bar():
    return rx.hstack(
        rx.vstack(
            rx.text(mini_txt("lang_label"), font_size="0.75rem", color=T.TEXT_SECONDARY),
            rx.select(
                ["vi", "en"],
                value=FolderState.ui_lang,
                on_change=FolderState.set_ui_lang,
                width="100px",
                border=f"1px solid {T.BORDER}",
                border_radius=T.RADIUS_MD,
            ),
            spacing="1",
            align="start",
        ),
        rx.vstack(
            rx.text(mini_txt("answer_mode_label"), font_size="0.75rem", color=T.TEXT_SECONDARY),
            rx.select(
                ["Native", "Foreign"],
                value=FolderState.answer_language,
                on_change=FolderState.set_answer_language,
                width="180px",
                border=f"1px solid {T.BORDER}",
                border_radius=T.RADIUS_MD,
            ),
            spacing="1",
            align="start",
        ),
        spacing="4",
        flex_wrap="wrap",
        width="100%",
    )
