import sys
from enum import Enum

import pygame as pg

import constants
from grid import Grid
from tower import Tower


class GameState(Enum):
    SETUP_PHASE = 'setup'
    BUILDING_TOWER = 'building'
    RUNNING_ROUND = 'running'


class Game:
    def __init__(self, game_name: str):
        pg.init()
        self.fps_clock = pg.time.Clock()
        self.screen = pg.display.set_mode(constants.SCREEN_SIZE)
        self.screen.fill(constants.BACKGROUND_COLOR)
        pg.display.set_caption(game_name)

        self.grid = Grid()
        self.state = GameState.SETUP_PHASE
        self.rounds_complete = 0

        # TODO: define starting money, etc

        self.towers = self.initialize_tower_images()
        self.selected_tower = 0

    def initialize_tower_images(self) -> list[dict]:
        # TODO: have different types of tower to choose from
        towers = []
        for i in range(1):
            towers.append(
                Tower(i, (self.grid.cell_size - 4, self.grid.cell_size - 4)))

        return towers

    def update(self):
        self.grid.update(self.screen)

        if self.state == GameState.BUILDING_TOWER:
            row, col = self.grid.get_cell_at(pg.mouse.get_pos())
            self.grid.show_tower(
                self.screen, self.towers[self.selected_tower], row, col)

        self.fps_clock.tick(constants.FPS)
        pg.display.update()

    def start_building_tower(self):
        self.state = GameState.BUILDING_TOWER

    def try_build_tower(self):
        # TODO: Check and discount any money to build tower
        row, col = self.grid.get_cell_at(pg.mouse.get_pos())
        if self.grid.is_cell_available_to_build(row, col):
            self.grid.build_tower(row, col, self.towers[self.selected_tower])
            self.state = GameState.SETUP_PHASE

    def cancel_building(self):
        self.state = GameState.SETUP_PHASE

    def start_round(self):
        self.state = GameState.RUNNING_ROUND


def main():
    game = Game(constants.GAME_NAME)

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if game.state == GameState.SETUP_PHASE:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_b:
                        game.start_building_tower()
                    elif event.key == pg.K_SPACE:
                        game.start_round()

            elif game.state == GameState.BUILDING_TOWER:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        game.cancel_building()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    game.try_build_tower()

        game.update()


if __name__ == '__main__':
    main()
