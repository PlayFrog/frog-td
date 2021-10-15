import pygame as pg


class Tower:
    def __init__(self, index: int, display_size: tuple[int, int]):
        self.main_sprite = pg.transform.scale(pg.image.load(
            f'assets/frog-{index}.png').convert_alpha(), display_size)
        self.invalid_sprite = pg.transform.scale(pg.image.load(
            f'assets/frog-{index}-invalid.png').convert_alpha(), display_size)
