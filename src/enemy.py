import pygame as pg


class Enemy:
    def __init__(self, hit_points: int, speed: int, filename: str = None,  display_size: tuple[int, int] = None, sprite: pg.Surface = None, padding: int = 0):
        if sprite:
            self.main_sprite = sprite
        else:
            self.main_sprite = pg.transform.scale(pg.image.load(
                f'assets/enemies/{filename}.png').convert_alpha(), display_size)
        self.padding = padding
        self.hp = hit_points
        self.speed = speed
        self.update_millis = 1000 / speed

    @staticmethod
    def create_enemies(cell_size: int):
        paddings = [16]
        ladybug = Enemy(200, 1, 'ladybug', (cell_size -
                        paddings[0], cell_size - paddings[0]), padding=paddings[0])

        return [ladybug]

    def set_speed(self, speed: int):
        self.speed = speed
        self.update_millis = 1000 / speed
