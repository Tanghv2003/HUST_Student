import reflex as rx

from HUST_Student.components.folder.blast_overlay import blast_overlay
from HUST_Student.components.folder.blocks_overlay import blocks_overlay
from HUST_Student.components.folder.edit_studyset_overlay import edit_studyset_overlay
from HUST_Student.components.folder.flashcard_overlay import flashcard_overlay
from HUST_Student.components.folder.match_overlay import match_overlay
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
        # Overlays / modals
        set_options_modal(),
        test_options_modal(),
        test_run_modal(),
        result_overlay(),
        flashcard_overlay(),
        match_overlay(),
        blast_overlay(),
        blocks_overlay(),
        learn_overlay(),
        edit_studyset_overlay(),

        # Header
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.icon("folder-open", size=18, color=T.WARN),
                    rx.text(
                        NavigationState.current_folder,
                        font_size="1.4rem",
                        font_weight="800",
                        color=T.TEXT_PRIMARY,
                        letter_spacing="-0.02em",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.text(
                    "Chọn học phần để bắt đầu học",
                    font_size="0.85rem",
                    color=T.TEXT_SECONDARY,
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.text(
                rx.foreach(
                    FolderState.current_sets,
                    lambda _: rx.fragment(),
                ),
                font_size="0.8rem",
                color=T.TEXT_MUTED,
            ),
            width="100%",
            align="center",
        ),

        # Studysets grid — 2 columns, compact cards
        rx.box(
            rx.grid(
                rx.foreach(
                    FolderState.current_sets,
                    lambda item: studyset_card(item.title, item.terms),
                ),
                template_columns="repeat(2, minmax(0, 1fr))",
                gap="3",
                width="100%",
            ),
            width="100%",
            overflow_y="auto",
            flex="1",
        ),

        width="100%",
        height="100%",
        spacing="4",
        align="start",
    )