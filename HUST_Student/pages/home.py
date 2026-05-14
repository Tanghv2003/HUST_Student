import reflex as rx

from HUST_Student.components.sidebar import sidebar
from HUST_Student.components.topbar import topbar
from HUST_Student.components.study_card import study_card
from HUST_Student.components.recent_item import recent_item


def home():

    return rx.box(

        sidebar(),

        rx.box(

            rx.vstack(

                topbar(),

                rx.vstack(

                    rx.text(
                        "Jump back in",
                        font_size="2rem",
                        font_weight="700",
                    ),

                    rx.grid(

                        study_card("Tính từ N4 thông dụng"),

                        study_card("Danh sách động từ N5, N4"),

                        columns="2",

                        spacing="6",

                        width="100%",
                    ),

                    spacing="6",

                    width="100%",
                ),

                rx.vstack(

                    rx.hstack(

                        rx.text(
                            "Recents",
                            font_size="2rem",
                            font_weight="700",
                        ),

                        rx.spacer(),

                        rx.link(
                            "Xem tất cả",
                            color="#4F46E5",
                        ),

                        width="100%",
                    ),

                    rx.grid(

                        recent_item(
                            "Tính từ N4 thông dụng",
                            "140 cards • by you",
                        ),

                        recent_item(
                            "Từ vựng N4",
                            "1138 cards • by Dorr1207",
                        ),

                        recent_item(
                            "Danh sách động từ N5, N4",
                            "Folder • by you",
                        ),

                        recent_item(
                            "Day 12",
                            "60 cards • by dovanthai92",
                        ),

                        columns="2",

                        spacing="4",

                        width="100%",
                    ),

                    spacing="5",

                    width="100%",
                ),

                spacing="8",

                width="100%",
            ),

            margin_left="280px",

            padding="2rem",

            bg="#FCFCFD",

            min_height="100vh",
        ),
    )