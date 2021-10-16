import pygame as pg


class Tower:
    def __init__(self, name: str, filename: str, display_size: tuple[int, int], price: int, damage: int, shooting_range: int):
        self.main_sprite = pg.transform.scale(pg.image.load(
            f'assets/towers/{filename}/sprite.png').convert_alpha(), display_size)
        self.invalid_sprite = pg.transform.scale(pg.image.load(
            f'assets/towers/{filename}/invalid.png').convert_alpha(), display_size)
        self.name = name
        self.price = price
        self.damage = damage
        self.range = shooting_range
