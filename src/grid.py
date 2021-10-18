import pygame as pg

import constants
from state import CellState
from tower import Tower


class Cell:
    def __init__(self, size: int, index: tuple[int, int], initial_state=None):
        self.state = initial_state if initial_state is not None else CellState.default()
        self.size = size
        self.index = index
        self.unit = None

    def display(self, surf: pg.Surface):
        pos = (self.index[1] * self.size, self.index[0] * self.size)

        color = constants.CONSTRUCTABLE_PATH_COLOR
        if self.state == CellState.OBSTACLE:
            color = constants.BACKGROUND_COLOR
        elif self.state == CellState.ENEMY_PATH:
            color = constants.ENEMY_PATH_COLOR

        rect = pg.Rect(pos, (self.size, self.size))
        pg.draw.rect(surf, color, rect)

        if self.state == CellState.TOWER:
            surf.blit(self.unit.main_sprite, pos)
        elif self.state == CellState.ENEMY:
            raise NotImplementedError()

    def highlight(self, surf: pg.Surface, color: tuple[int, int, int]):
        # Highlights the cell at position
        row, col = self.index
        x, y = col * self.size, row * self.size

        highlight_thickness = 2

        for offset in [0, self.size - highlight_thickness]:
            # Horizontal highlight
            highlight_rect = pg.Rect(
                x, y + offset, self.size, highlight_thickness)
            pg.draw.rect(surf, color, highlight_rect)

            # Vertical highlight
            highlight_rect = pg.Rect(
                x + offset, y, highlight_thickness, self.size)
            pg.draw.rect(surf, color, highlight_rect)

    def show_radius(self, surf: pg.Surface, radius: int = None):
        if not radius:
            if not self.unit:
                return
            radius = self.unit.range
        row, col = self.index
        rgba_surf = pg.Surface((radius * 2, radius * 2),  pg.SRCALPHA)
        pg.draw.circle(rgba_surf, constants.YELLOW_TRANSLUCID,
                       (radius, radius), radius)
        x, y = self.size * col - \
            (radius - self.size // 2), self.size * \
            row - (radius - self.size // 2)
        surf.blit(rgba_surf, (x, y))

    def build_tower(self, tower: Tower):
        self.unit = tower
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
        self.show_radius = False

    def pre_update(self, surf: pg.Surface):
        for row in self.grid:
            for cell in row:
                cell.display(surf)

    def post_update(self, surf: pg.Surface):
        for row in self.grid:
            for cell in row:
                if self.show_radius:
                    cell.show_radius(surf)

    def get_cell_at(self, pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos
        if x > constants.SCREEN_SIZE[0] or y > constants.SCREEN_SIZE[1]:
            return (None, None)

        col = round(((x - self.cell_size / 2) /
                    constants.SCREEN_SIZE[0]) * self.NUM_COLS)
        row = round(((y - self.cell_size / 2) /
                    constants.SCREEN_SIZE[1]) * self.NUM_ROWS)

        return (row, col)

    def is_cell_available_to_build(self, row, col) -> bool:
        if row is None and col is None:
            return False
        return self.grid[row][col].state == CellState.CONSTRUCTABLE_PATH

    def show_tower(self, surf: pg.Surface, tower: Tower, pos: tuple[int, int]):
        row, col = self.get_cell_at(pos)
        if row is None and col is None:
            return

        if self.is_cell_available_to_build(row, col):
            sprite = tower.main_sprite
            highlight_color = constants.GREEN
        else:
            sprite = tower.invalid_sprite
            highlight_color = constants.RED

        self.grid[row][col].highlight(surf, highlight_color)
        self.grid[row][col].show_radius(surf, tower.range)

        x, y = pos
        surf.blit(sprite, (x - sprite.get_width() //
                           2, y - sprite.get_height() // 2))

    def build_tower(self, row: int, col: int, tower: Tower):
        if row is None and col is None:
            return
        self.grid[row][col].build_tower(tower)
