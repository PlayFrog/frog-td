import pygame as pg

import constants
from state import GameState
from tower import Tower


class UI:
    def __init__(self, screen: pg.Surface, fonts: list[pg.font.Font]):
        self.screen = screen
        self.screen.fill('black')
        self.fonts = fonts
        self.show_instructions = False
        self.warning = None

    def display_information_panel(self, state: GameState, available_coins: int,
                                  rounds_complete: int):
        info_panel_surf = pg.Surface(
            (constants.SCREEN_SIZE[0], constants.INFO_PANEL_HEIGHT))
        padding = 4

        coin_text = self.fonts[0].render(
            f'Moedas disponíveis: {available_coins}', False, constants.COIN_COLOR)
        info_panel_surf.blit(coin_text, (padding, padding))

        game_mode_text = self.fonts[0].render(
            f'Modo: {state}', False, constants.WHITE)
        info_panel_surf.blit(
            game_mode_text, (padding, constants.INFO_PANEL_HEIGHT // 2 + padding))

        round_text = self.fonts[0].render(
            f"Rounds completos: {rounds_complete}", False, constants.WHITE)
        info_panel_surf.blit(
            round_text, (constants.SCREEN_SIZE[0] -
                         (round_text.get_width() + padding), padding)
        )

        if self.warning:
            warning_text = self.fonts[0].render(
                self.warning, False, constants.RED)
            info_panel_surf.blit(
                warning_text, (constants.SCREEN_SIZE[0] - (
                    warning_text.get_width() + padding), constants.INFO_PANEL_HEIGHT // 2 + padding)
            )

        self.screen.blit(info_panel_surf, (0, constants.SCREEN_SIZE[1]))

    def display_instructions_sign(self):
        inst_sign_surf = pg.Surface(
            (constants.SCREEN_SIZE[0], constants.INSTRUCTIONS_SIGN_HEIGHT))
        inst_sign_surf.fill('black')
        text = self.fonts[0].render(
            "Pressione 'h' para ver as instruções", False, constants.ENEMY_PATH_COLOR)
        inst_sign_surf.blit(text, (constants.SCREEN_SIZE[0] // 2 - text.get_width(
        ) // 2, constants.INSTRUCTIONS_SIGN_HEIGHT // 2 - text.get_height() // 2))
        self.screen.blit(
            inst_sign_surf, (0, constants.SCREEN_SIZE[1] + constants.INFO_PANEL_HEIGHT))

    def display_tower_info(self, tower: Tower):
        tower_info_surf = pg.Surface(
            (constants.SCREEN_SIZE[0], constants.INSTRUCTIONS_SIGN_HEIGHT))
        tower_info_surf.fill('black')
        padding = 4

        name = self.fonts[1].render(
            tower.name, False, constants.WHITE)
        tower_info_surf.blit(name, (constants.SCREEN_SIZE[0] // 2 - name.get_width(
        ) // 2, padding))

        data = self.fonts[0].render(
            f"Preço: {tower.price}   Dano: {tower.damage}   Área: {tower.range}",
            False, constants.ENEMY_PATH_COLOR)
        tower_info_surf.blit(data, (constants.SCREEN_SIZE[0] // 2 - data.get_width(
        ) // 2,  name.get_height() + padding * 2))

        self.screen.blit(
            tower_info_surf, (0, constants.SCREEN_SIZE[1] + constants.INFO_PANEL_HEIGHT))

    def display_instructions_modal(self):
        instructions_modal = pg.Surface(constants.INSTRUCTIONS_MODAL_SIZE)
        instructions_modal.fill(constants.GRAY)
        padding_y = 4
        padding_x = 16

        title = self.fonts[1].render("Instruções", False, constants.WHITE)
        instructions_modal.blit(title,
                                (constants.INSTRUCTIONS_MODAL_SIZE[0] // 2 - title.get_width() // 2,
                                 padding_y))

        for i, txt in enumerate(constants.INSTRUCTIONS):
            instruction_txt = self.fonts[0].render(
                txt, False, constants.WHITE)
            instructions_modal.blit(
                instruction_txt, (padding_x, title.get_height() + padding_y * (i + 2) +
                                  instruction_txt.get_height() * (i + 1)))

        self.screen.blit(instructions_modal,
                         (constants.SCREEN_SIZE[0] // 2 - constants.INSTRUCTIONS_MODAL_SIZE[0] // 2,
                          constants.SCREEN_SIZE[1] // 2 - constants.INSTRUCTIONS_MODAL_SIZE[1] // 2)
                         )

    def set_warning(self, message: str):
        self.warning = message

    def update(self, state: GameState, available_coins: int, rounds_complete: int,
               selected_tower: Tower):
        self.display_information_panel(state, available_coins, rounds_complete)
        if self.show_instructions:
            self.display_instructions_modal()
        if state == GameState.BUILDING_TOWER:
            self.display_tower_info(selected_tower)
        else:
            self.display_instructions_sign()
