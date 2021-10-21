import pygame as pg

import constants
from enemy import Enemy
from linked_list import Node
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
        elif self.state == CellState.ENEMY_PATH or self.state == CellState.ENEMY:
            color = constants.ENEMY_PATH_COLOR
        elif self.state == CellState.PATH_START:
            color = constants.ENEMY_PATH_START_COLOR
        elif self.state == CellState.PATH_END:
            color = constants.ENEMY_PATH_END_COLOR

        rect = pg.Rect(pos, (self.size, self.size))
        pg.draw.rect(surf, color, rect)

        if self.state == CellState.TOWER or self.state == CellState.ENEMY:
            unit_pos = pos[0] + self.unit.padding // 2, pos[1] + \
                self.unit.padding // 2
            surf.blit(self.unit.main_sprite, unit_pos)

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
            if self.state != CellState.TOWER:
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

    def push_enemy(self, enemy: Enemy):
        if self.state == CellState.ENEMY:
            existing_enemy = self.unit
        else:
            self.state = CellState.ENEMY
            existing_enemy = None

        if enemy is None:
            self.state = CellState.ENEMY_PATH
        else:
            self.unit = enemy
        return existing_enemy


class Grid:
    NUM_ROWS = 15
    NUM_COLS = 20

    def __init__(self, level_name: str):
        if constants.SCREEN_SIZE[1] // self.NUM_ROWS != constants.SCREEN_SIZE[0] // self.NUM_COLS:
            raise ValueError("Cells must be squared")

        grid: list[list[Cell]] = []
        
        x_start : int = -1
        x_end   : int = -1

        y_start : int = -1
        y_end   : int = -1

        self.cell_size = constants.SCREEN_SIZE[0] // self.NUM_COLS
        state_grid = self.load_from_file(level_name)

        for i in range(self.NUM_ROWS):
            row = []
            for j in range(self.NUM_COLS):
                cell = Cell(self.cell_size, (i, j), initial_state=state_grid[i][j])
                if state_grid[i][j] == CellState.PATH_START:
                    self.enemy_path : Node = Node(cell)
                    x_start, y_start = i, j
                elif (state_grid[i][j] == CellState.PATH_END):
                    x_end, y_end = i, j
                row.append(cell)
            grid.append(row)
        assert(x_start != -1 and x_end != -1 and y_start != -1, y_end != -1)
        self.grid = grid
        self.show_radius = False
        self.create_enemy_path(x_start, y_start, x_end, y_end, self.enemy_path, None)
        

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

    def push_enemies(self, new_enemy: Enemy = None):
        cursor = self.enemy_path
        enemy = new_enemy
        while cursor is not None:
            enemy = cursor.item.push_enemy(enemy)
            cursor = cursor.next

    def create_enemy_path(self, x_start: int, y_start: int, x_end: int, y_end: int, result: Node, from_cell: Cell = None):
        def check_indices(i, j) -> bool:
            return i >= 0 and i < self.NUM_ROWS and j < self.NUM_COLS and j>=0

        def find_next_cell(i, j, from_cell) -> Cell:
            if check_indices(i-1, j) and from_cell.index != self.grid[i-1][j].index and self.grid[i-1][j].state == CellState.ENEMY_PATH or self.grid[i-1][j].state == CellState.PATH_END:
                return self.grid[i-1][j] # path on top
            if check_indices(i+1, j) and from_cell.index != self.grid[i+1][j].index and self.grid[i+1][j].state == CellState.ENEMY_PATH or self.grid[i+1][j].state == CellState.PATH_END:
                return self.grid[i+1][j] # path on bottom
            if check_indices(i, j-1) and from_cell.index != self.grid[i][j-1].index and self.grid[i][j-1].state == CellState.ENEMY_PATH or  self.grid[i][j-1].state == CellState.PATH_END:
                return self.grid[i][j-1] # path on left 
            if check_indices(i, j+1) and from_cell.index != self.grid[i][j+1].index and self.grid[i][j+1].state == CellState.ENEMY_PATH or self.grid[i][j+1].state == CellState.PATH_END:
                return self.grid[i][j+1] # path on right
            else:
                return None
        if x_start == x_end and y_start == y_end:
            return
        else:
            if from_cell == None:
                from_cell = result.item
            result.next = Node(find_next_cell(x_start, y_start, from_cell))
            x, y = result.next.item.index
            self.create_enemy_path(x, y, x_end, y_end, result.next, result.item)
            

    def load_from_file(self, level_name: str):
        grid: list[list[CellState]] = [[None for x in range(self.NUM_COLS)] for y in range(self.NUM_ROWS)]
        
        file = open(f'assets/levels/{level_name}.txt')
        rows, cols = file.readline().split(" ")
        rows, cols = int(rows), int(cols)

        for i in range(rows):
            line = file.readline().strip()
            assert(len(line) == cols)
            for j, ch in enumerate(line):
                grid[i][j] = CellState.from_char(ch)
        return grid

        
