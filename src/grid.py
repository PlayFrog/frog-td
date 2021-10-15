from enum import Enum

import pygame as pg

import constants
from tower import Tower


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
        self.sprite = None

    def display(self, surf: pg.Surface):
        pos = (self.index[1] * self.size, self.index[0] * self.size)
        if self.state == CellState.TOWER:
            surf.blit(self.sprite, pos)
        elif self.state == CellState.ENEMY:
            raise NotImplementedError()
        else:
            if self.state == CellState.CONSTRUCTABLE_PATH:
                color = constants.CONSTRUCTABLE_PATH_COLOR
            elif self.state == CellState.OBSTACLE:
                color = constants.BACKGROUND_COLOR
            elif self.state == CellState.ENEMY_PATH:
                color = constants.ENEMY_PATH_COLOR

            rect = pg.Rect(pos, (self.size, self.size))
            pg.draw.rect(surf, color, rect)

    def build_tower(self, tower: Tower):
        self.sprite = tower.main_sprite
        self.state = CellState.TOWER


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

    def update(self, surf: pg.Surface):
        for row in self.grid:
            for cell in row:
                cell.display(surf)

    def get_cell_at(self, pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos

        col = round(((x - self.cell_size / 2) /
                    constants.SCREEN_SIZE[0]) * self.NUM_COLS)
        row = round(((y - self.cell_size / 2) /
                    constants.SCREEN_SIZE[1]) * self.NUM_ROWS)

        return (row, col)

    def is_cell_available_to_build(self, row, col) -> bool:
        return self.grid[row][col].state == CellState.CONSTRUCTABLE_PATH

    def show_tower(self, surf: pg.Surface, tower: Tower, row: int, col: int):
        x, y = col * self.cell_size, row * self.cell_size

        if self.is_cell_available_to_build(row, col):
            sprite = tower.main_sprite
        else:
            sprite = tower.invalid_sprite

        surf.blit(sprite, (x, y))

    def build_tower(self, row: int, col: int, tower: Tower):
        self.grid[row][col].build_tower(tower)

    def highlight_cell(self, surf: pg.Surface, pos: tuple[int, int]):
        # Highlights the cell at position
        row, col = self.get_cell_at(pos)
        x, y = col * self.cell_size, row * self.cell_size

        highlight_thickness = 4
        highlight_color = (244, 234, 122)

        for offset in [0, self.cell_size - highlight_thickness]:
            # Horizontal highlight
            highlight_rect = pg.Rect(
                x, y + offset, self.cell_size, highlight_thickness)
            pg.draw.rect(surf, highlight_color, highlight_rect)

            # Vertical highlight
            highlight_rect = pg.Rect(
                x + offset, y, highlight_thickness, self.cell_size)
            pg.draw.rect(surf, highlight_color, highlight_rect)
