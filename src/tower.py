import pygame as pg


class Tower:
    def __init__(self, name: str, index: int, display_size: tuple[int, int], price: int, damage: int):
        self.main_sprite = pg.transform.scale(pg.image.load(
            f'assets/towers/{index}.png').convert_alpha(), display_size)
        self.invalid_sprite = pg.transform.scale(pg.image.load(
            f'assets/towers/{index}-invalid.png').convert_alpha(), display_size)
        self.name = name
        self.price = price
        self.damage = damage
