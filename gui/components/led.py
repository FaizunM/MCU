import pygame

class LED:
    def __init__(self, board_pin, pin, x, y, color):
        self.board_pin = board_pin
        self.pin = pin
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        image_path = None
        
        state = self.board_pin.get_pin(self.pin)
        if state:
            if self.color == "RED":
                image_path = "./assets/led_on_red.png"
            if self.color == "GREEN":
                image_path = "./assets/led_on_green.png"
            if self.color == "YELLOW":
                image_path = "./assets/led_on_yellow.png"
        else:
            image_path = "./assets/led_off.png"

        original = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(
            original, (original.get_width() / original.get_height() * 9, 9)
        )
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        surface.blit(self.image, self.rect)
