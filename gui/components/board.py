import pygame

class Board:
    def __init__(self, x, y, image_path):
        original = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(
            original, (original.get_width() / original.get_height() * 360, 360)
        )
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
