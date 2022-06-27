import pygame as pg

import constants
from enemy import Enemy
from grid import Grid
from tower import Tower


class Round:
    def __init__(self, enemy: Enemy, quantity: int, round_reward: int):
        self.enemy = enemy
        self.remaining = quantity
        self.round_reward = round_reward
        self.last_update = pg.time.get_ticks()

        self.current_enemies: list[Enemy] = []
        self.passed_enemies = 0
        self.rewards = 0
        self.complete = False

    @staticmethod
    def create_rounds(enemies):
        i = 0
        rounds: list[Round] = []
        for round_index in range(constants.NUM_ROUNDS):
            enemy = Enemy(enemies[i].hp, enemies[i].speed, enemies[i].reward,
                          sprite=enemies[i].main_sprite, padding=enemies[i].padding)
            enemy.hp += round_index * 25
            # Additional HP later on
            if round_index >= 10 and round_index < 20:
                enemy.hp += round_index * 10
            elif round_index >= 20:
                enemy.hp += round_index * 20
            enemy.reward += min(round_index * 5, 40)
            enemy.set_speed(enemy.speed + round(round_index * 0.3))

            quantity = 5 + round_index * 1

            round_reward = 150 + min(round_index * 25, 200)
            # Bonus rounds
            if round_index == 10:
                round_reward += 500
            elif round_index == 20:
                round_reward += 2000

            # Boss in last round
            if round_index == constants.NUM_ROUNDS - 1:
                enemy = Enemy(hit_points=500000, speed=0.5, reward=0,
                              sprite=enemies[i].main_sprite, padding=-10)
                quantity = 1
                round_reward = 0

            new_round = Round(enemy, quantity, round_reward)

            i = (i + 1) % len(enemies)
            rounds.append(new_round)

        return rounds

    def update(self, grid: Grid, towers: list[Tower], screen: pg.Surface):
        time = pg.time.get_ticks()
        i = 0
        for tower in towers:
            i += 1
            tower.update(self.current_enemies, screen)

        # Remove dead enemies
        for i, enemy in enumerate(self.current_enemies):
            if enemy.dead:
                row, col = enemy.index
                self.rewards += enemy.reward
                grid.kill_enemy(row, col)
                self.current_enemies.pop(i)
                if len(self.current_enemies) == 0 and self.remaining == 0:
                    self.end()

        # Add more enemies and remove passed
        if self.last_update + self.enemy.update_millis < time:
            self.last_update = time
            if self.remaining > 0:
                new_enemy = self.enemy.copy()
                grid.push_enemy(new_enemy)
                self.current_enemies.append(new_enemy)
                self.remaining -= 1
            else:
                passed = grid.push_enemy()
                if passed:
                    self.current_enemies.pop()
                    self.passed_enemies += 1
                    if len(self.current_enemies) == 0:
                        self.end()
                        grid.push_enemy()

    def end(self):
        for enemy in self.current_enemies:
            del(enemy)
        self.current_enemies = []
        self.complete = True

    def is_complete(self):
        return self.complete
