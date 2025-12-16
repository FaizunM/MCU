import pygame
import sys

class Board:
    def __init__(self, x, y, image_path):
        original = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(
            original, (original.get_width() / original.get_height() * 360, 360)
        )
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class PushButton:
    def __init__(self, x, y, image_path):
        original = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(original, (25, 25))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class LED:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.state = False

    def update_state(self, state):
        self.state = state 
        
    def draw(self, surface):
        image_path = None
        if self.state:
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


class PowerButton:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.state = False
        
    def update_state(self, state):
        self.state = state 

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text_render = font.render(f"{'ON' if self.state else 'OFF'}", True, (0, 0, 0))
        text_rect = text_render.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )
        screen.blit(text_render, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Window:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.screen_width = 640
        self.screen_height = 360
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("MCU Board View")
        self.clock = pygame.time.Clock()
        self.running = True

        self.board = Board(0, 0, "./assets/board.png")
        self.reset_button = PushButton(78, 26, "./assets/push_btn.png")

        self.power_state = False

        self.power_led = LED( 411, 115, "GREEN")
        self.builtin_led = LED(219, 86, "RED")
        self.builtin_led.state = True
        self.tx_led = LED(219, 114, "YELLOW")
        self.rx_led = LED(219, 127, "YELLOW")

        self.font = pygame.font.Font(None, 14)

        self.power_pin = [0, 0, 3.3, 5.0, 0, 0, 0]
        self.analog_pin = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.digital_pin = [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ]
        self.power_btn = PowerButton(
            self.screen_width - 80 - 10,
            self.screen_height - 40 - 10,
            80,
            40,
            (200, 200, 200),
        )
    
    def get_power_state(self):
        return self.power_state

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.reset_button.is_clicked(event.pos):
                        print("CLICKED")
                    if self.power_btn.is_clicked(event.pos):
                        if self.power_state:
                            self.power_state = False
                        else:
                            self.power_state = True

    def update(self):
        self.power_btn.update_state(self.power_state)
        self.power_led.update_state(self.power_state)

    def draw(self):
        self.screen.fill((200, 218, 234))

        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_render = self.font.render(
            f"X: {self.mouse_pos[0]} Y: {self.mouse_pos[1]}", True, (0, 0, 0)
        )
        self.screen.blit(self.mouse_render, (10, 10))

        power_label = ["IOREF", "RESET", "3.3V", "5V", "GND", "GND", "VIN"]
        for num in range(0, 7):
            power_render = self.font.render(
                f"{power_label[num]}: {self.power_pin[num]}", True, (0, 0, 0)
            )
            self.screen.blit(power_render, (500, 10 + num * 14))

        analog_label = ["A0", "A1", "A2", "A3", "A4", "A5"]
        for num in range(0, 6):
            analog_render = self.font.render(
                f"{analog_label[num]}: {self.analog_pin[num]}", True, (0, 0, 0)
            )
            self.screen.blit(analog_render, (550, 10 + num * 14))

        digital_label = [
            "D0",
            "D1",
            "D2",
            "D3",
            "D4",
            "D5",
            "D6",
            "D7",
            "D8",
            "D9",
            "D10",
            "D11",
            "D12",
            "D13",
        ]
        for num in range(0, 14):
            digital_render = self.font.render(
                f"{digital_label[num]}: {self.digital_pin[num]}", True, (0, 0, 0)
            )
            self.screen.blit(digital_render, (550, 100 + num * 14))

        self.board.draw(self.screen)
        self.reset_button.draw(self.screen)

        self.power_led.draw(self.screen)
        self.builtin_led.draw(self.screen)
        self.tx_led.draw(self.screen)
        self.rx_led.draw(self.screen)

        self.power_btn.draw(self.screen, self.font)

        pygame.display.flip()


if __name__ == "__main__":
    window = Window()
    window.run()
    pygame.quit()
    sys.exit()
