import reflex as rx

from HUST_Student.core.i18n import STRINGS
from HUST_Student.states.folder_state import FolderState


def mini_txt(key: str):
    return rx.cond(
        FolderState.ui_lang == "en",
        STRINGS["en"].get(key, key),
        STRINGS["vi"].get(key, key),
    )
