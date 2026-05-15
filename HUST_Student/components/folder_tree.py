import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.states.folder_state import FolderState
from HUST_Student.states.navigation_state import NavigationState


def folder_node(
    name: str,
    data: dict,
    level: int = 0,
):
    folders = data.get(
        "folders",
        {},
    )

    return rx.vstack(
        rx.hstack(
            rx.icon("folder", size=18, color=T.WARN),
            rx.text(
                name,
                font_weight="600",
                color=T.TEXT_PRIMARY,
                font_size="0.95rem",
            ),
            spacing="3",
            align="center",
            width="100%",
            padding="0.7rem 1rem",
            border_radius=T.RADIUS_MD,
            cursor="pointer",
            transition="background 0.12s ease",
            on_click=lambda: [
                FolderState.open_folder(name),
                NavigationState.set_folder_detail(name),
            ],
            _hover={
                "bg": T.PRIMARY_TINT,
            },
        ),
        rx.cond(
            len(folders) > 0,
            rx.vstack(
                *[
                    folder_node(child_name, child_data, level + 1)
                    for child_name, child_data in folders.items()
                ],
                spacing="1",
                width="100%",
                padding_left=f"{(level + 1) * 24}px",
            ),
        ),
        spacing="1",
        align="start",
        width="100%",
    )
