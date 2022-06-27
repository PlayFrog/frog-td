import pygame as pg

import constants
from enemy import Enemy
from grid import Grid
from rounds import Round
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
        self.grid = Grid("level2")
        self._ui = UI(self.screen, self.fonts)
        self.state = GameState.SETUP_PHASE

        self.available_coins = starting_coins
        self.current_round_coins = 0
        self.current_round_enemies_passed = 0

        print("[Initializing] Loading tower images...")
        self.tower_options = Tower.create_towers(self.grid.cell_size)
        self.selected_tower = 0

        print("[Initializing] Setting up rounds...")
        self.lifes = constants.STARTING_LIFES
        self.enemies = Enemy.create_enemies(self.grid.cell_size)
        self.rounds = Round.create_rounds(self.enemies)
        self.rounds_complete = 0
        self.existing_towers: list[Tower] = []

        print("[Running] Game starting")

    def toggle_instructions(self):
        self._ui.show_instructions = not self._ui.show_instructions

    def close_instructions(self):
        self._ui.show_instructions = False

    def update(self):
        self.grid.pre_update(self.screen)

        if self.state == GameState.BUILDING_TOWER:
            twr = self.tower_options[self.selected_tower]
            self.grid.show_tower(
                self.screen, twr, pg.mouse.get_pos(), self.available_coins)

        elif self.state == GameState.RUNNING_ROUND:
            self.rounds[self.rounds_complete].update(
                self.grid, self.existing_towers, self.screen)
            if self.rounds[self.rounds_complete].rewards > self.current_round_coins:
                self.current_round_coins = self.rounds[self.rounds_complete].rewards
            if self.rounds[self.rounds_complete].passed_enemies > self.current_round_enemies_passed:
                self.decrease_life()
                self.current_round_enemies_passed += 1
            if self.rounds[self.rounds_complete].is_complete():
                self.available_coins += self.current_round_coins
                self.available_coins += self.rounds[self.rounds_complete].round_reward
                self.current_round_coins = 0
                self.current_round_enemies_passed = 0
                self.rounds_complete += 1
                if self.rounds_complete == len(self.rounds):
                    self.state = GameState.WON
                else:
                    self.state = GameState.SETUP_PHASE

        self._ui.update(self.state, self.available_coins + self.current_round_coins,
                        self.rounds_complete, self.tower_options[self.selected_tower], self.lifes)

        self.grid.post_update(self.screen)
        self.fps_clock.tick(constants.FPS)
        pg.display.update()

    def start_building_tower(self):
        self.state = GameState.BUILDING_TOWER

    def increase_selected_tower(self):
        self.selected_tower = (
            self.selected_tower + 1) % len(self.tower_options)

    def decrease_selected_tower(self):
        self.selected_tower = (
            self.selected_tower - 1) % len(self.tower_options)

    def try_build_tower(self):
        tower = self.tower_options[self.selected_tower].copy()
        row, col = self.grid.get_cell_at(pg.mouse.get_pos())

        if not self.grid.is_cell_available_to_build(row, col):
            self._ui.set_warning("Local de construção inválido")
            return

        if self.available_coins < tower.price:
            self._ui.set_warning("Moedas insuficientes")
            return

        self._ui.set_warning(None)
        self.available_coins -= tower.price
        tower.position = (row * self.grid.cell_size, col * self.grid.cell_size)
        print('[Running] Tower built at position:', tower.position)
        self.existing_towers.append(tower)
        self.grid.build_tower(row, col, tower)
        self.state = GameState.SETUP_PHASE

    def cancel_building(self):
        self._ui.set_warning(None)
        self.state = GameState.SETUP_PHASE

    def start_round(self):
        self.state = GameState.RUNNING_ROUND

    def decrease_life(self):
        print('[Running] Enemy passed!')
        self.lifes -= 1
        if self.lifes == 0:
            self.state = GameState.LOST

    def game_over(self):
        self._ui.show_game_over()

    def win(self):
        self._ui.show_victory()

    def show_tower_radius(self):
        self.grid.show_radius = not self.grid.show_radius
        pg.display.update()
