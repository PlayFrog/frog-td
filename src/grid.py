from enum import Enum

import pygame

import constants


class CellState(Enum):
    ENEMY = 'enemy'
    TOWER = 'tower'
    CONSTRUCTABLE_PATH = 'constructable_path'
    ENEMY_PATH = 'enemy_path'
    OBSTACLE = 'obstacle'


def default_cell_state() -> CellState:
    return CellState.CONSTRUCTABLE_PATH


class Cell:
    def __init__(self, size: int, index: tuple[int, int], initial_state=None):
        self.state = initial_state if initial_state is not None else default_cell_state()
        self.size = size
        self.index = index

    def display(self, surf: pygame.Surface):
        if self.state == CellState.CONSTRUCTABLE_PATH:
            color = constants.CONSTRUCTABLE_PATH_COLOR
        elif self.state == CellState.OBSTACLE:
            color = constants.BACKGROUND_COLOR
        elif self.state == CellState.ENEMY_PATH:
            color = constants.ENEMY_PATH_COLOR
        else:
            raise NotImplementedError()

        rect = pygame.Rect(
            (self.index[1] * self.size, self.index[0] * self.size), (self.size, self.size))
        pygame.draw.rect(surf, color, rect)


class Grid:
    NUM_ROWS = 15
    NUM_COLS = 20

    def __init__(self):
        if constants.SCREEN_SIZE[1] // self.NUM_ROWS != constants.SCREEN_SIZE[0] // self.NUM_COLS:
            raise ValueError("Cells must be squared")

        grid: list[list[Cell]] = []

        self.cell_size = constants.SCREEN_SIZE[0] // self.NUM_COLS

        for i in range(self.NUM_ROWS):
            row = []
            for j in range(self.NUM_COLS):
                # TODO: Create a better enemy path
                if j == self.NUM_COLS // 2:
                    row.append(Cell(self.cell_size, (i, j),
                               initial_state=CellState.ENEMY_PATH))
                else:
                    row.append(Cell(self.cell_size, (i, j)))
            grid.append(row)

        self.grid = grid

    def display(self, surf: pygame.Surface):
        for row in self.grid:
            for cell in row:
                cell.display(surf)
