from math import dist

import pygame as pg

from constants import TONGUE_COLOR
from enemy import Enemy


class Tower:
    def __init__(self, name: str, filename: str, display_size: tuple[int, int], price: int,
                 damage: int, shooting_range: int, padding: int = 0, speed: float = 1.):
        self.main_sprite = pg.transform.scale(pg.image.load(
            f'assets/towers/{filename}/sprite.png').convert_alpha(), display_size)
        self.invalid_sprite = pg.transform.scale(pg.image.load(
            f'assets/towers/{filename}/invalid.png').convert_alpha(), display_size)
        self.name = name
        self.price = price
        self.damage = damage
        self.range = shooting_range
        self.padding = padding
        self.speed = speed
        self.last_shot = pg.time.get_ticks()
        self.position = (0, 0)

    @staticmethod
    def create_towers(cell_size=int):
        paddings = [8, 4, 1]
        mini_toad = Tower("Mini-Toad", "mini-toad",
                          (cell_size - paddings[0], cell_size - paddings[0]), 100, 5, 50, padding=paddings[0], speed=1.2)
        toad = Tower("Toad", "toad", (cell_size -
                     paddings[1], cell_size - paddings[1]), 200, 15, 50, padding=paddings[1])
        monster_toad = Tower("Monster Toad", "monster-toad",
                             (cell_size - paddings[2], cell_size - paddings[2]), 400, 45, 75, padding=paddings[2])

        return [mini_toad, toad, monster_toad]

    def update(self, enemies: list[Enemy], screen: pg.Surface):
        now = pg.time.get_ticks()
        if now - self.last_shot >= 1000 / self.speed:
            for enemy in enemies:
                distance = dist(enemy.get_position(), self.position)
                if distance <= self.range:
                    self.shoot(enemy, screen)
                    self.last_shot = now
                    break

    def shoot(self, enemy: Enemy, screen: pg.Surface):
        print("Shooting!")
        enemy.hit(self.damage)
        tongue = pg.Surface(
            (abs(self.position[0] - enemy.position[0]), abs(self.position[1] - enemy.position[1])))
        tongue.fill(TONGUE_COLOR)

        screen.blit(tongue, enemy.position)
