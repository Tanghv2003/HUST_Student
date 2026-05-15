import reflex as rx

from HUST_Student.components.folder.flashcard_overlay import flashcard_overlay
from HUST_Student.components.folder.set_options_modal import set_options_modal
from HUST_Student.components.folder.studyset_card import studyset_card
from HUST_Student.components.learn.overlay import learn_overlay
from HUST_Student.components.test.options_modal import test_options_modal
from HUST_Student.components.test.result_overlay import result_overlay
from HUST_Student.components.test.run_modal import test_run_modal
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
        rx.text(
            NavigationState.current_folder,
            font_size="2.5rem",
            font_weight="700",
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
