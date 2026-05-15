import reflex as rx

from HUST_Student.components.folder.mini_game_toolbar import mini_settings_bar
from HUST_Student.components.folder.mini_i18n import mini_txt
from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.states.folder_state import FolderState


def blocks_overlay():
    header = rx.vstack(
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
        mini_settings_bar(),
        rx.hstack(
            rx.text(mini_txt("blocks_remaining"), font_weight="600", color=T.TEXT_PRIMARY),
            rx.text(FolderState.blocks_remaining, font_weight="800", color=T.PRIMARY),
            rx.spacer(),
            rx.text(mini_txt("blocks_cleared"), font_weight="600", color=T.TEXT_SECONDARY),
            rx.text(FolderState.blocks_cleared, font_weight="700", color=T.TEXT_SECONDARY),
            width="100%",
            flex_wrap="wrap",
        ),
        spacing="3",
        width="100%",
    )

    play = rx.vstack(
        header,
        rx.box(
            rx.text(
                FolderState.blocks_top_prompt,
                font_size="1.85rem",
                font_weight="800",
                color=T.TEXT_PRIMARY,
                text_align="center",
            ),
            padding="2rem",
            width="100%",
            min_height="160px",
            display="flex",
            align_items="center",
            justify_content="center",
            border=f"1px solid {T.BORDER}",
            border_radius=T.RADIUS_XL,
            bg=T.SURFACE,
            box_shadow=T.SHADOW_CARD,
        ),
        rx.input(
            placeholder=mini_txt("blocks_type"),
            value=FolderState.blocks_input,
            on_change=FolderState.set_blocks_input,
            size="3",
            width="100%",
            border=f"1px solid {T.BORDER}",
            border_radius=T.RADIUS_MD,
            padding="0.9rem 1rem",
        ),
        rx.cond(
            FolderState.blocks_feedback == "wrong",
            rx.text(mini_txt("blocks_wrong_rotate"), color=T.DANGER, font_size="0.9rem", font_weight="600"),
            rx.box(),
        ),
        rx.button(
            mini_txt("blast_send"),
            on_click=FolderState.submit_blocks,
            bg=T.PRIMARY,
            color="white",
            border_radius=T.RADIUS_PILL,
            font_weight="700",
            width="100%",
            padding="0.9rem",
            _hover={"bg": T.PRIMARY_HOVER},
        ),
        spacing="4",
        width="100%",
    )

    done = rx.vstack(
        header,
        rx.box(
            rx.text(
                mini_txt("blocks_done"),
                font_size="1.15rem",
                font_weight="700",
                color=T.TEXT_PRIMARY,
                text_align="center",
            ),
            rx.hstack(
                rx.text(mini_txt("blocks_cleared"), ": ", FolderState.blocks_cleared, font_weight="600"),
                rx.text("·", color=T.TEXT_MUTED),
                rx.text(mini_txt("blast_stat_wrong"), ": ", FolderState.blocks_wrong, font_weight="600"),
                justify="center",
                width="100%",
                margin_top="0.75rem",
                color=T.TEXT_SECONDARY,
            ),
            padding="1.5rem",
            width="100%",
            border_radius=T.RADIUS_LG,
            bg=T.SUCCESS_BG,
            border=f"1px solid {T.SUCCESS}",
        ),
        rx.hstack(
            rx.button(
                mini_txt("common_again"),
                on_click=FolderState.restart_blocks,
                bg=T.SURFACE,
                color=T.TEXT_PRIMARY,
                border=f"1px solid {T.BORDER}",
                border_radius=T.RADIUS_PILL,
                font_weight="600",
            ),
            rx.button(
                mini_txt("common_close"),
                on_click=FolderState.close_blocks,
                bg=T.BORDER_LIGHT,
                color=T.TEXT_PRIMARY,
                border_radius=T.RADIUS_MD,
                font_weight="600",
            ),
            spacing="3",
        ),
        spacing="4",
        width="100%",
    )

    return rx.cond(
        FolderState.show_blocks,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.cond(FolderState.blocks_phase == "complete", done, play),
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
