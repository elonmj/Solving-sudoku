from enum import Enum
from dataclasses import dataclass


class Color(Enum):
    BEIGE = (202, 194, 186)
    BLACK = (0, 0, 0)
    CORAL = (255, 127, 8)
    GREEN = (79, 159, 77)
    WHITE = (225, 225, 225)
    BUTTON = (100, 149, 237)
    BUTTON_HOVER = (75, 119, 190)


@dataclass
class Config:
    WINDOW_SIZE: tuple[int, int] = (360, 360)
    PADDING: int = 10
    BUTTON_HEIGHT: int = 30
    BUTTON_WIDTH: int = 100
    CELL_FONT_SIZE: int = 22
    TIMER_FONT_SIZE: int = 16
    GAME_OVER_FONT_SIZE: int = 32
    ANIMATION_DELAY: int = 500
    FPS: int = 60
    FONT_PATH: str = "assets/fonts/OpenSans-Medium.ttf"


# Instance globale de la configuration
GameConfig = Config()

