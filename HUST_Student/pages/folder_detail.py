import reflex as rx

from HUST_Student.components.folder.flashcard_overlay import flashcard_overlay
from HUST_Student.components.folder.set_options_modal import set_options_modal
from HUST_Student.components.folder.studyset_card import studyset_card
from HUST_Student.components.learn.overlay import learn_overlay
from HUST_Student.components.test.options_modal import test_options_modal
from HUST_Student.components.test.result_overlay import result_overlay
from HUST_Student.components.test.run_modal import test_run_modal
from HUST_Student.components.ui import theme as T
from HUST_Student.states.folder_state import FolderState
from HUST_Student.states.navigation_state import NavigationState


def folder_detail_page():
    return rx.vstack(
        set_options_modal(),
        test_options_modal(),
        test_run_modal(),
        result_overlay(),
        flashcard_overlay(),
        learn_overlay(),
        rx.vstack(
            rx.text(
                NavigationState.current_folder,
                font_size="2rem",
                font_weight="800",
                color=T.TEXT_PRIMARY,
                letter_spacing="-0.02em",
            ),
            rx.text(
                "Chọn một học phần để học hoặc kiểm tra.",
                font_size="0.95rem",
                color=T.TEXT_SECONDARY,
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        rx.vstack(
            rx.foreach(
                FolderState.current_sets,
                lambda item: studyset_card(item.title, item.terms),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        spacing="6",
    )
