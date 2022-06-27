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
        self.max_hp = hit_points
        self.reward = reward
        self.speed = speed
        self.update_millis = 1000 / speed
        self.position = None
        self.dead = False

    @staticmethod
    def create_enemies(cell_size: int):
        paddings = [16]
        ladybug = Enemy(hit_points=50, speed=2, reward=40, filename='ladybug', display_size=(cell_size -
                        paddings[0], cell_size - paddings[0]), padding=paddings[0])
        beetle = Enemy(hit_points=100, speed=1, reward=20, filename='beetle',
                       display_size=(cell_size, cell_size), padding=0)
        butterfly = Enemy(hit_points=70, speed=3, reward=60, filename='butterfly', display_size=(
            cell_size, cell_size), padding=0)
        spider = Enemy(hit_points=200, speed=1, reward=20, filename='spider',
                       display_size=(cell_size, cell_size), padding=0)

        return [ladybug, beetle, ladybug, butterfly, ladybug, spider]

    def copy(self):
        return Enemy(self.hp, self.speed, self.reward, sprite=self.main_sprite, padding=self.padding)

    def set_speed(self, speed: int):
        self.speed = speed
        self.update_millis = 1000 / speed

    def hit(self, damage: int):
        self.hp -= damage
        if self.hp < 0:
            self.dead = True

    def get_position(self) -> tuple[int, int]:
        if self.position is None:
            raise RuntimeError("Enemy has no position!")
        return self.position
