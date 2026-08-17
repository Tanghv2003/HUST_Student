import reflex as rx

from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_state import FolderState


def blocks_options_modal():
    return rx.cond(
        FolderState.show_blocks_options,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                FolderState.selected_set.title,
                                font_size="1.4rem",
                                font_weight="800",
                                color=T.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Thiết lập Khối hợp",
                                color=T.TEXT_SECONDARY,
                                font_size="0.95rem",
                            ),
                            spacing="1",
                            align="start",
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_blocks_options),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    rx.vstack(
                        rx.text(
                            "Mỗi lượt hiện 4 thẻ ngẫu nhiên — nhấn thẻ để lật.",
                            font_size="0.88rem",
                            color=T.TEXT_SECONDARY,
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text(
                                    "Xuất hiện trước",
                                    font_weight="600",
                                    color=T.TEXT_PRIMARY,
                                ),
                                rx.select(
                                    ["Ngoại ngữ (Foreign)", "Bản xứ (Native)"],
                                    value=rx.cond(
                                        FolderState.blocks_first_lang == "native",
                                        "Bản xứ (Native)",
                                        "Ngoại ngữ (Foreign)",
                                    ),
                                    on_change=FolderState.set_blocks_first_lang_from_ui,
                                    width="200px",
                                    border=f"1px solid {T.BORDER}",
                                    border_radius=T.RADIUS_MD,
                                    padding="0.9rem 1rem",
                                ),
                                spacing="2",
                                align="start",
                            ),
                            spacing="8",
                            width="100%",
                        ),
                        rx.button(
                            "Bắt đầu",
                            on_click=FolderState.start_blocks,
                            bg=T.PRIMARY,
                            color="white",
                            font_weight="700",
                            border_radius=T.RADIUS_PILL,
                            padding="1rem 1.5rem",
                            width="100%",
                            _hover={"bg": T.PRIMARY_HOVER, "cursor": "pointer"},
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    spacing="6",
                    padding="2rem",
                    width="100%",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="480px",
                max_width="min(480px, calc(100vw - 2.5rem))",
                max_height=T.MODAL_CONTENT_MAX_HEIGHT,
                min_height="0",
                overflow_y="auto",
                overflow_x="hidden",
                border=f"1px solid {T.BORDER}",
                box_shadow=T.SHADOW_MODAL,
                on_click=rx.stop_propagation,
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            display="flex",
            align_items="center",
            justify_content="center",
            bg=T.OVERLAY_SCRIM,
            z_index="999",
            padding=T.MODAL_OVERLAY_PADDING,
            on_click=FolderState.close_blocks_options,
        ),
        rx.box(),
    )
