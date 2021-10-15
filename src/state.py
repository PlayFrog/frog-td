from enum import Enum
from typing import Literal


class GameState(Enum):
    SETUP_PHASE = 'setup'
    BUILDING_TOWER = 'building'
    RUNNING_ROUND = 'running'

    def __str__(self):
        if self == GameState.SETUP_PHASE:
            return "Standby"
        if self == GameState.BUILDING_TOWER:
            return "Construção"
        if self == GameState.RUNNING_ROUND:
            return "Round em execução"

        raise NotImplementedError(f"__str__ not implemented for {self}")


class CellState(Enum):
    ENEMY = 'enemy'
    TOWER = 'tower'
    CONSTRUCTABLE_PATH = 'constructable_path'
    ENEMY_PATH = 'enemy_path'
    OBSTACLE = 'obstacle'

    @staticmethod
    def default_cell_state() -> Literal:
        return CellState.CONSTRUCTABLE_PATH