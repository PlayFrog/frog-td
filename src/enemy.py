from typing import Optional
import pygame as pg
from constants import SCREEN_SIZE


class Enemy:
    def __init__(self, hit_points: int, speed: int, reward: int, filename: Optional[str] = None,
                 display_size: tuple[int, int] = SCREEN_SIZE, sprite: Optional[pg.surface.Surface] = None, padding: int = 0):
        self.main_sprite = sprite or pg.transform.scale(pg.image.load(
                f'assets/enemies/{filename}.png').convert_alpha(), display_size)
        self.padding = padding
        self.hp = hit_points
        self.reward = reward
        self.speed = speed
        self.update_millis = 1000 / speed

    @staticmethod
    def create_enemies(cell_size: int):
        paddings = [16]
        ladybug = Enemy(200, 1, 40, 'ladybug', (cell_size -
                        paddings[0], cell_size - paddings[0]), padding=paddings[0])

        return [ladybug]

    def set_speed(self, speed: int):
        self.speed = speed
        self.update_millis = 1000 / speed

    def hit(self, damage: int):
        self.hp -= damage
