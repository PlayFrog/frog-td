import sys

import pygame as pg

import constants
from game import Game
from state import GameState


def main():
    game = Game(constants.GAME_NAME, starting_coins=constants.STARTING_COINS)

    running = True

    while running:
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
                    if event.key == pg.K_r:
                        game.show_tower_radius()
            elif event.type == pg.MOUSEBUTTONDOWN:
                game.close_instructions()

            if game.state == GameState.SETUP_PHASE:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_b:
                        game.start_building_tower()
                    elif event.key == pg.K_SPACE:
                        if len(game.existing_towers) == 0:
                            game.start_building_tower()
                        else:
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

            elif game.state == GameState.WON or game.state == GameState.LOST:
                running = False

        game.update()

    if game.state == GameState.WON:
        game.win()
    elif game.state == GameState.LOST:
        game.game_over()
    game.fps_clock.tick(constants.FPS)

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.display.update()


if __name__ == '__main__':
    main()
