import pygame as pg

import constants
from grid import Grid
from state import GameState
from tower import Tower
from ui import UI


class Game:
    def __init__(self, game_name: str, starting_coins=200):
        print("[Initializing] Starting Pygame...")
        pg.init()

        # Load font
        print("[Initializing] Loading fonts...")
        pg.font.init()
        self.font_sm = pg.font.Font(
            'assets/fonts/Inconsolata-Regular.ttf', 22)
        self.font_md = pg.font.Font(
            'assets/fonts/Inconsolata-Regular.ttf', 32)
        self.font_lg = pg.font.Font(
            'assets/fonts/Inconsolata-Regular.ttf', 64)
        self.fonts = [self.font_sm, self.font_md, self.font_lg]

        # Setup metadata
        print("[Initializing] Setting game up...")
        self.fps_clock = pg.time.Clock()
        w, h = constants.SCREEN_SIZE
        self.screen = pg.display.set_mode(
            (w, h + constants.INFO_PANEL_HEIGHT + constants.INSTRUCTIONS_SIGN_HEIGHT))
        pg.display.set_caption(game_name)

        # Start game logic
        self.grid = Grid()
        self._ui = UI(self.screen, self.fonts)
        self.state = GameState.SETUP_PHASE
        self.rounds_complete = 0

        self.available_coins = starting_coins

        print("[Initializing] Loading tower images...")
        self.towers = self.initialize_tower_images()
        self.selected_tower = 0

        print("[Running] Game starting")

    def initialize_tower_images(self) -> list[Tower]:
        towers = []
        towers.append(Tower("Mini-Toad", "mini-toad", (self.grid.cell_size -
                      4, self.grid.cell_size - 4), 100, 5, 50))
        towers.append(Tower("Toad", "toad", (self.grid.cell_size -
                      4, self.grid.cell_size - 4), 200, 15, 50))
        towers.append(Tower("Monster Toad", "monster-toad", (self.grid.cell_size -
                      4, self.grid.cell_size - 4), 400, 45, 75))

        return towers

    def toggle_instructions(self):
        self._ui.show_instructions = not self._ui.show_instructions

    def close_instructions(self):
        self._ui.show_instructions = False

    def update(self):
        self.grid.pre_update(self.screen)

        if self.state == GameState.BUILDING_TOWER:
            twr = self.towers[self.selected_tower]
            self.grid.show_tower(self.screen, twr, pg.mouse.get_pos())

        self._ui.update(self.state, self.available_coins,
                        self.rounds_complete, self.towers[self.selected_tower])

        self.grid.post_update(self.screen)
        self.fps_clock.tick(constants.FPS)
        pg.display.update()

    def start_building_tower(self):
        self.state = GameState.BUILDING_TOWER

    def increase_selected_tower(self):
        self.selected_tower = (
            self.selected_tower + 1) % len(self.towers)

    def decrease_selected_tower(self):
        self.selected_tower = (
            self.selected_tower - 1) % len(self.towers)

    def try_build_tower(self):
        tower = self.towers[self.selected_tower]
        row, col = self.grid.get_cell_at(pg.mouse.get_pos())

        if not self.grid.is_cell_available_to_build(row, col):
            self._ui.set_warning("Local de construção inválido")
            return

        if self.available_coins < tower.price:
            self._ui.set_warning("Moedas insuficientes")
            return

        self._ui.set_warning(None)
        self.available_coins -= tower.price
        self.grid.build_tower(row, col, tower)
        self.state = GameState.SETUP_PHASE

    def cancel_building(self):
        self._ui.set_warning(None)
        self.state = GameState.SETUP_PHASE

    def start_round(self):
        self.state = GameState.RUNNING_ROUND

    def show_tower_radius(self):
        self.grid.show_radius = not self.grid.show_radius
