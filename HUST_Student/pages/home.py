import reflex as rx

from HUST_Student.components.sidebar import sidebar
from HUST_Student.components.topbar import topbar

from HUST_Student.pages.library import library_page
from HUST_Student.pages.classes import classes_page
from HUST_Student.pages.folder_detail import folder_detail_page

from HUST_Student.states.navigation_state import NavigationState


def homepage_content():

    return rx.vstack(

        rx.text(
            "Homepage",
            font_size="3rem",
            font_weight="700",
        ),

        width="100%",
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

                classes_page(),
            ),
        ),
    )


def home():

    return rx.box(

        sidebar(),

        rx.box(

            rx.vstack(

                topbar(),

                content_router(),

                spacing="8",

                width="100%",
            ),

            margin_left="280px",

            padding="2rem",

            bg="#F6F7FB",

            min_height="100vh",
        ),
    )