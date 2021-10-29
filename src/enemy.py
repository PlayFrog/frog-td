import pygame as pg


class Enemy:
    def __init__(self, hit_points: int, speed: int, reward: int, filename: str = None,
                 display_size: tuple[int, int] = None, sprite: pg.Surface = None, padding: int = 0):
        if sprite:
            self.main_sprite = sprite
        else:
            self.main_sprite = pg.transform.scale(pg.image.load(
                f'assets/enemies/{filename}.png').convert_alpha(), display_size)
        self.padding = padding
        self.hp = hit_points
        self.reward = reward
        self.speed = speed
        self.update_millis = 1000 / speed
        self.position = None
        self.dead = False

    @staticmethod
    def create_enemies(cell_size: int):
        paddings = [16]
        ladybug = Enemy(50, 2, 40, 'ladybug', (cell_size -
                        paddings[0], cell_size - paddings[0]), padding=paddings[0])

        return [ladybug]

    def copy(self):
        return Enemy(self.hp, self.speed, self.reward, sprite=self.main_sprite, padding=self.padding)

    def set_speed(self, speed: int):
        self.speed = speed
        self.update_millis = 1000 / speed

    def hit(self, damage: int):
        self.hp -= damage
        if self.hp < 0:
            print("Enemy died!")
            self.dead = True
        else:
            print("Shot enemy now has", self.hp, "hp")

    def get_position(self) -> tuple[int, int]:
        if self.position is None:
            raise RuntimeError("Enemy has no position!")
        return self.position
