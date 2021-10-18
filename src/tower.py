import pygame as pg


class Tower:
    def __init__(self, name: str, filename: str, display_size: tuple[int, int], price: int,
                 damage: int, shooting_range: int, padding: int = 0):
        self.main_sprite = pg.transform.scale(pg.image.load(
            f'assets/towers/{filename}/sprite.png').convert_alpha(), display_size)
        self.invalid_sprite = pg.transform.scale(pg.image.load(
            f'assets/towers/{filename}/invalid.png').convert_alpha(), display_size)
        self.name = name
        self.price = price
        self.damage = damage
        self.range = shooting_range
        self.padding = padding

    @staticmethod
    def create_towers(cell_size=int):
        paddings = [8, 4, 1]
        mini_toad = Tower("Mini-Toad", "mini-toad",
                          (cell_size - paddings[0], cell_size - paddings[0]), 100, 5, 50, padding=paddings[0])
        toad = Tower("Toad", "toad", (cell_size -
                     paddings[1], cell_size - paddings[1]), 200, 15, 50, padding=paddings[1])
        monster_toad = Tower("Monster Toad", "monster-toad",
                             (cell_size - paddings[2], cell_size - paddings[2]), 400, 45, 75, padding=paddings[2])

        return [mini_toad, toad, monster_toad]
