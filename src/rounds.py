import pygame as pg

import constants
from enemy import Enemy
from grid import Grid


class Round:
    def __init__(self, enemy: Enemy, quantity: int):
        self.enemy = enemy
        self.remaining = quantity
        self.last_update = pg.time.get_ticks()

    @staticmethod
    def create_rounds(enemies):
        i = 0
        rounds: list[Round] = []
        for round_index in range(constants.NUM_ROUNDS):
            enemy = Enemy(enemies[i].hp, enemies[i].speed,
                          sprite=enemies[i].main_sprite, padding=enemies[i].padding)
            enemy.hp += round_index * 100
            enemy.set_speed(enemy.speed + round(round_index * 0.3))

            quantity = 5 + round_index * 1

            _round = Round(enemy, quantity)

            i = (i + 1) % len(enemies)
            rounds.append(_round)

        return rounds

    def update(self, grid: Grid):
        time = pg.time.get_ticks()
        if self.last_update + self.enemy.update_millis < time:
            self.last_update = time
            if self.remaining > 0:
                grid.push_enemies(self.enemy)
                self.remaining -= 1
            else:
                grid.push_enemies()
