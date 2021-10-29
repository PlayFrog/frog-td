import pygame as pg

import constants
from enemy import Enemy
from grid import Grid
from tower import Tower


class Round:
    def __init__(self, enemy: Enemy, quantity: int):
        self.enemy = enemy
        self.remaining = quantity
        self.last_update = pg.time.get_ticks()

        self.current_enemies: list[Enemy] = []

    @staticmethod
    def create_rounds(enemies):
        i = 0
        rounds: list[Round] = []
        for round_index in range(constants.NUM_ROUNDS):
            enemy = Enemy(enemies[i].hp, enemies[i].speed, enemies[i].reward,
                          sprite=enemies[i].main_sprite, padding=enemies[i].padding)
            enemy.hp += round_index * 25
            enemy.reward += round_index * 10
            enemy.set_speed(enemy.speed + round(round_index * 0.3))

            quantity = 5 + round_index * 1

            _round = Round(enemy, quantity)

            i = (i + 1) % len(enemies)
            rounds.append(_round)

        return rounds

    def update(self, grid: Grid, towers: list[Tower], screen: pg.Surface):
        time = pg.time.get_ticks()
        for tower in towers:
            tower.update(self.current_enemies, screen)

        # Remove dead enemies
        for i, enemy in enumerate(self.current_enemies):
            if enemy.dead:
                row, col = enemy.index
                grid.kill_enemy(row, col)
                self.current_enemies.pop(i)

        # Add more enemies
        if self.last_update + self.enemy.update_millis < time:
            self.last_update = time
            if self.remaining > 0:
                new_enemy = self.enemy.copy()
                grid.push_enemies(new_enemy)
                self.current_enemies.append(new_enemy)
                self.remaining -= 1
            else:
                grid.push_enemies()

    def end(self):
        for enemy in self.current_enemies:
            del(enemy)
        self.current_enemies = []
