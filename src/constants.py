import pygame as pg

# Screen and game settings
SCREEN_SIZE = (800, 600)
FPS = 30
GAME_NAME = 'Frog TD'
NUM_ROUNDS = 30
STARTING_LIFES = 10
STARTING_COINS = 600

# UI
INSTRUCTIONS_MODAL_SIZE = (SCREEN_SIZE[0] - 128, SCREEN_SIZE[1] - 64)
INFO_PANEL_HEIGHT = 64
INSTRUCTIONS_SIGN_HEIGHT = 64
HP_BAR_HEIGHT = 4

# Colors
CONSTRUCTABLE_PATH_COLOR = pg.Color(130, 76, 48)
ENEMY_PATH_COLOR = pg.Color(201, 154, 118)
ENEMY_PATH_START_COLOR = pg.Color(100, 255, 100)
ENEMY_PATH_END_COLOR = pg.Color(255, 100, 100)
BACKGROUND_COLOR = pg.Color(27, 114, 5)
COIN_COLOR = pg.Color(234, 186, 28)
TONGUE_COLOR = pg.Color(250, 128, 124)
GREEN = pg.Color(0, 255, 0)
YELLOW = pg.Color(244, 234, 122)
YELLOW_TRANSLUCID = pg.Color(244, 234, 122, 122)
WHITE = pg.Color(255, 255, 255)
BLACK = pg.Color(0, 0, 0)
GRAY = pg.Color(90, 90, 90)
RED = pg.Color(255, 0, 0)

INSTRUCTIONS = [
    "No modo de Standby...",
    "Pressione 'b' para construir uma torre.",
    "Pressione 'espaço' para começar um round.",
    "",
    "No modo de Construção...",
    "Pressione '<-' e '->' para alterar torres.",
    "Clique para construir.",
    "Pressione 'esc' para cancelar.",
    "",
    "Em qualquer modo...",
    "Pressione 'r' para ativar a visualização de área de ataque",
    "das torres."
]
