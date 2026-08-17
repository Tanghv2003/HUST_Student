import reflex as rx

from HUST_Student.components.folder.mini_i18n import mini_txt
from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_state import FolderState


def _block_card(card: rx.Var):
    face_text = rx.cond(
        FolderState.blocks_first_lang == "native",
        card.back,
        card.front,
    )
    back_text = rx.cond(
        FolderState.blocks_first_lang == "native",
        card.front,
        card.back,
    )
    display_text = rx.cond(card.is_flipped, back_text, face_text)

    return rx.box(
        rx.text(
            display_text,
            font_size="1.05rem",
            font_weight="700",
            color=T.TEXT_PRIMARY,
            text_align="center",
            line_height="1.4",
        ),
        padding="1.25rem",
        width="100%",
        min_height="120px",
        display="flex",
        align_items="center",
        justify_content="center",
        border=f"1px solid {T.BORDER}",
        border_radius=T.RADIUS_LG,
        bg=rx.cond(card.is_flipped, T.PRIMARY_LIGHT, T.SURFACE),
        box_shadow=T.SHADOW_CARD,
        cursor="pointer",
        transition="all 0.15s ease",
        on_click=[rx.stop_propagation, FolderState.flip_block_card(card.card_id)],
        _hover={"border_color": T.PRIMARY, "transform": "translateY(-2px)"},
    )


def blocks_overlay():
    settings_bar = rx.hstack(
        rx.vstack(
            rx.text(
                rx.cond(FolderState.ui_lang == "vi", "Ngôn ngữ", "Language"),
                font_size="0.75rem",
                color=T.TEXT_SECONDARY,
                font_weight="700",
            ),
            rx.select(
                ["vi", "en"],
                value=FolderState.ui_lang,
                on_change=FolderState.set_ui_lang,
                width="90px",
                border=f"1px solid {T.BORDER}",
                border_radius=T.RADIUS_MD,
            ),
            spacing="1",
            align="start",
        ),
        rx.vstack(
            rx.text(
                rx.cond(FolderState.ui_lang == "vi", "Thẻ mới", "Reset"),
                font_size="0.75rem",
                color=T.TEXT_SECONDARY,
                font_weight="700",
            ),
            rx.button(
                rx.icon("rotate-ccw", size=15),
                "Reset",
                on_click=FolderState.restart_blocks,
                bg=T.SURFACE,
                color=T.TEXT_PRIMARY,
                border=f"1px solid {T.BORDER}",
                border_radius=T.RADIUS_MD,
                font_weight="600",
                height="32px",
                _hover={"bg": T.BORDER_LIGHT},
            ),
            spacing="1",
            align="start",
        ),
        spacing="4",
        flex_wrap="wrap",
        width="100%",
    )

    return rx.cond(
        FolderState.show_blocks,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                rx.cond(FolderState.selected_set, FolderState.selected_set.title, ""),
                                font_size="1.2rem",
                                font_weight="800",
                                color=T.TEXT_PRIMARY,
                            ),
                            rx.text(mini_txt("blocks_title"), font_size="0.95rem", font_weight="700", color=T.PRIMARY),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_blocks),
                        width="100%",
                        align="center",
                    ),
                    rx.text(mini_txt("blocks_sub"), font_size="0.88rem", color=T.TEXT_SECONDARY),
                    settings_bar,
                    rx.hstack(
                        rx.text(mini_txt("blocks_card_count"), font_weight="600", color=T.TEXT_PRIMARY),
                        rx.text(FolderState.blocks_card_count, font_weight="800", color=T.PRIMARY),
                        spacing="2",
                        width="100%",
                    ),
                    rx.grid(
                        rx.foreach(FolderState.blocks_cards, _block_card),
                        columns="2",
                        gap="3",
                        width="100%",
                    ),
                    rx.text(
                        mini_txt("blocks_flip_hint"),
                        font_size="0.82rem",
                        color=T.TEXT_MUTED,
                        text_align="center",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="640px",
                max_width="min(640px, calc(100vw - 2.5rem))",
                max_height=T.MODAL_CONTENT_MAX_HEIGHT,
                min_height="0",
                overflow_y="auto",
                overflow_x="hidden",
                border=f"1px solid {T.BORDER}",
                box_shadow=T.SHADOW_MODAL,
                padding="2rem",
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
            on_click=FolderState.close_blocks,
        ),
        rx.box(),
    )
