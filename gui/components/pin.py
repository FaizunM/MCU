import pygame

class Pin:
    def __init__(self, board_pin, idx, x, y, width, height, color):
        self.board_pin = board_pin
        self.idx = idx
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shown_text = False
        
    def show_text(self):
        self.shown_text = True
        
    def hide_text(self):
        self.shown_text = False

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.shown_text:
            text_render = font.render(f"{self.idx}: {self.board_pin.get_pin(self.idx)}", True, (0, 0, 0))
            screen.blit(text_render, (10, 20))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)