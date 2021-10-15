import sys

import pygame

import constants
from grid import Grid


class Game:
    def __init__(self, game_name: str):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)
        self.screen.fill(constants.BACKGROUND_COLOR)
        pygame.display.set_caption(game_name)

        self.grid = Grid()

    def update(self):
        self.fps_clock.tick(constants.FPS)
        self.grid.display(self.screen)
        pygame.display.update()


def main():
    game = Game(constants.GAME_NAME)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.update()


if __name__ == '__main__':
    main()
