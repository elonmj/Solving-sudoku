import pygame
from ..config import Color, GameConfig

class Button:
    def __init__(self, x: int, y: int, text: str):
        self.rect = pygame.Rect(x, y, GameConfig.BUTTON_WIDTH, GameConfig.BUTTON_HEIGHT)
        self.text = text
        self.is_hovered = False

    def draw(self, screen: pygame.Surface) -> None:
        color = Color.BUTTON_HOVER.value if self.is_hovered else Color.BUTTON.value
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, Color.BLACK.value, self.rect, 1)

        font = pygame.font.Font(GameConfig.FONT_PATH, 18)
        text = font.render(self.text, True, Color.WHITE.value)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

class Grid:
    def __init__(self, board, padding: int, offset_y: int):
        self.board = board
        self.padding = padding
        self.offset_y = offset_y
        self.rects = {}
        self.selected_cell = None

__all__ = ["Button", "Grid"]