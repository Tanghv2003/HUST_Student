import reflex as rx

from HUST_Student.components.folder.mini_game_toolbar import mini_settings_bar
from HUST_Student.components.folder.mini_i18n import mini_txt
from HUST_Student.components.ui import theme as T
from HUST_Student.components.ui.modal import modal_close_btn
from HUST_Student.models.mini_game import MatchTile
from HUST_Student.states.folder_state import FolderState


def _match_tile_btn(tile: MatchTile):
    return rx.box(
        rx.text(
            tile.text,
            font_size="1rem",
            font_weight="600",
            color=T.TEXT_PRIMARY,
            text_align="center",
            white_space="normal",
            word_break="break-word",
        ),
        padding="1rem",
        min_height="88px",
        display="flex",
        align_items="center",
        justify_content="center",
        border_radius=T.RADIUS_LG,
        border=rx.cond(
            tile.matched,
            f"1px solid {T.BORDER}",
            rx.cond(
                FolderState.match_selected_tile_id == tile.tile_id,
                f"2px solid {T.PRIMARY}",
                f"1px solid {T.BORDER}",
            ),
        ),
        bg=rx.cond(tile.matched, T.BORDER_LIGHT, T.SURFACE),
        opacity=rx.cond(tile.matched, "0.5", "1"),
        cursor=rx.cond(tile.matched, "default", "pointer"),
        box_shadow=T.SHADOW_CARD,
        on_click=lambda: FolderState.match_pick(tile.tile_id),
        transition="border-color 0.12s ease, opacity 0.12s ease",
        _hover=rx.cond(tile.matched, {}, {"border_color": T.PRIMARY}),
    )


def match_overlay():
    return rx.cond(
        FolderState.show_match,
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
                            rx.text(
                                mini_txt("match_title"),
                                font_size="0.95rem",
                                font_weight="700",
                                color=T.PRIMARY,
                            ),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        modal_close_btn(FolderState.close_match),
                        width="100%",
                        align="center",
                    ),
                    rx.text(mini_txt("match_sub"), font_size="0.88rem", color=T.TEXT_SECONDARY),
                    mini_settings_bar(),
                    rx.hstack(
                        rx.text(mini_txt("match_pairs"), font_weight="600", color=T.TEXT_PRIMARY),
                        rx.text(
                            FolderState.match_pairs_done,
                            " / ",
                            FolderState.match_total_pairs,
                            font_weight="700",
                            color=T.TEXT_SECONDARY,
                        ),
                        spacing="2",
                    ),
                    rx.cond(
                        FolderState.match_all_matched,
                        rx.box(
                            mini_txt("match_done"),
                            padding="1rem",
                            border_radius=T.RADIUS_MD,
                            bg=T.SUCCESS_BG,
                            color=T.TEXT_PRIMARY,
                            width="100%",
                            font_weight="600",
                            border=f"1px solid {T.SUCCESS}",
                        ),
                        rx.box(),
                    ),
                    rx.grid(
                        rx.foreach(FolderState.match_tiles, _match_tile_btn),
                        template_columns="repeat(auto-fill, minmax(140px, 1fr))",
                        gap="3",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            mini_txt("common_again"),
                            on_click=FolderState.restart_match,
                            bg=T.SURFACE,
                            color=T.TEXT_PRIMARY,
                            border=f"1px solid {T.BORDER}",
                            border_radius=T.RADIUS_PILL,
                            font_weight="600",
                        ),
                        rx.button(
                            mini_txt("common_close"),
                            on_click=FolderState.close_match,
                            bg=T.BORDER_LIGHT,
                            color=T.TEXT_PRIMARY,
                            border_radius=T.RADIUS_MD,
                            font_weight="600",
                        ),
                        spacing="3",
                        flex_wrap="wrap",
                    ),
                    spacing="4",
                    width="100%",
                ),
                bg=T.SURFACE,
                border_radius=T.RADIUS_XL,
                width="760px",
                max_width="min(760px, calc(100vw - 2.5rem))",
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
            on_click=FolderState.close_match,
        ),
        rx.box(),
    )
