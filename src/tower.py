from math import dist

import pygame as pg

from constants import TONGUE_COLOR
from enemy import Enemy


class Tower:
    def __init__(self, name: str, filename: str, display_size: tuple[int, int], price: int,
                 damage: int, shooting_range: int, padding: int = 0, speed: float = 1., color: tuple[int, int, int] = TONGUE_COLOR):
        self.main_sprite = pg.transform.scale(pg.image.load(
            f'assets/towers/{filename}/sprite.png').convert_alpha(), display_size)
        self.invalid_sprite = pg.transform.scale(pg.image.load(
            f'assets/towers/{filename}/invalid.png').convert_alpha(), display_size)
        self.filename = filename
        self.display_size = display_size
        self.name = name
        self.price = price
        self.damage = damage
        self.range = shooting_range
        self.padding = padding
        self.speed = speed
        self.last_shot = pg.time.get_ticks()
        self.position = (0, 0)
        self.color = color

    @staticmethod
    def create_towers(cell_size=int):
        paddings = [8, 4, 2, 1, 0]
        mini_toad = Tower(name="Mini-Toad", filename="mini-toad",
                          display_size=(cell_size - paddings[0], cell_size - paddings[0]), price=100,
                          damage=25, shooting_range=100, padding=paddings[0], speed=1.25)
        toad = Tower(name="Toad", filename="toad", display_size=(cell_size -
                     paddings[1], cell_size - paddings[1]), price=200, damage=30, shooting_range=100,
                     padding=paddings[1], speed=2.)
        monster_toad = Tower(name="Monster Toad", filename="monster-toad",
                             display_size=(
                                 cell_size - paddings[2], cell_size - paddings[2]),
                             price=400, damage=100, shooting_range=125, padding=paddings[2])
        prince_frog = Tower(name="Prince Frog", filename="prince-frog",
                            display_size=(
                                 cell_size - paddings[3], cell_size - paddings[3]),
                            price=1000, damage=150, shooting_range=250, padding=paddings[3], speed=0.75)
        bug_disruptor = Tower(name="Bug Disruptor", filename="bug-disruptor",
                              display_size=(
                                  cell_size - paddings[4], cell_size - paddings[4]),
                              price=2000, damage=125, shooting_range=150, padding=paddings[4], speed=4.)
        frogod = Tower(name="FROGOD", filename="frogod",
                       display_size=(
                           cell_size - paddings[4], cell_size - paddings[4]),
                       price=10000, damage=500, shooting_range=200, padding=paddings[4], speed=8.)

        return [mini_toad, toad, monster_toad, prince_frog, bug_disruptor, frogod]

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
        enemy.hit(self.damage)

        # For some reason x and y are inverted here
        x, y = enemy.position
        x2, y2 = self.position
        pg.draw.line(screen, TONGUE_COLOR, (y2 + self.main_sprite.get_width() //
                     2, x2 + self.main_sprite.get_height() // 2), (y + enemy.main_sprite.get_width() // 2, x + enemy.main_sprite.get_height() // 2),
                     width=4)

    def copy(self):
        return Tower(name=self.name, filename=self.filename, display_size=self.display_size,
                     price=self.price, damage=self.damage, shooting_range=self.range, padding=self.padding, speed=self.speed,
                     color=self.color)
