# type: ignore
import pygame


class Platform:
    def __init__(self, x, y, width, height, level=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = level

        # Initialize font once per platform (or you can do this globally)
        self.font = pygame.font.SysFont(None, 24)  # Default font, size 24

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        rect = self.get_rect()
        pygame.draw.rect(screen, (100, 10, 200), rect)

        # Render the level number as text
        level_text = self.font.render(str(self.level - 4), True, (255, 255, 255))  # white color

        # Center the text inside the platform rectangle
        text_rect = level_text.get_rect(center=rect.center)

        # Draw the text on the screen
        screen.blit(level_text, text_rect)
