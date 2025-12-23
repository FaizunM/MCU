import pygame

class PowerButton:
    def __init__(self, state, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.state = state

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text_render = font.render(f"{'OFF' if self.state else 'ON'}", True, (0, 0, 0))
        text_rect = text_render.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )
        screen.blit(text_render, text_rect)

    def update(self, state):
        self.state = state

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class PushButton:
    def __init__(self, x, y, image_path):
        original = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(original, (25, 25))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

