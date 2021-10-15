import sys

import pygame as pg

import constants
from game import Game
from state import GameState


def main():
    game = Game(constants.GAME_NAME)

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # Open/close instructions independently of state
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    game.toggle_instructions()
                else:
                    game.close_instructions()
            elif event.type == pg.MOUSEBUTTONDOWN:
                game.close_instructions()

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
                    elif event.key == pg.K_LEFT:
                        game.decrease_selected_tower()
                    elif event.key == pg.K_RIGHT:
                        game.increase_selected_tower()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    game.try_build_tower()

        game.update()


if __name__ == '__main__':
    main()
