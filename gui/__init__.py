from gui.components.board import Board
from gui.components.button import PowerButton, PushButton
from gui.components.led import LED
from gui.components.pin import Pin

import pygame
import sys


class MCUBoardView:
    def __init__(self, mcu_board, board_pin):
        self.board_pin = board_pin
        self.mcu_board = mcu_board

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

        self.power_led = LED(self.board_pin, 4, 411, 115, "GREEN")
        self.builtin_led = LED(self.board_pin, 18, 219, 86, "RED")
        self.tx_led = LED(self.board_pin, 30, 219, 114, "RED")
        self.rx_led = LED(self.board_pin, 31, 219, 127, "RED")

        self.font = pygame.font.Font(None, 14)

        self.power_btn = PowerButton(
            self.mcu_board.board_power.is_plugged,
            self.screen_width - 80 - 10,
            self.screen_height - 40 - 10,
            80,
            40,
            (200, 200, 200),
        )

        self.pin_power = []

        for i in range(0, 8):
            self.pin_power.append(Pin(board_pin, i, 222 + (i * 15.5), 323, 7, 7, (0, 0, 0)))
        
        for i in range(0, 6):
            self.pin_power.append(Pin(board_pin, i + 8, 361 + (i * 15.5), 323, 7, 7, (0, 0, 0)))

        for i in range(0, 10):
            self.pin_power.append(Pin(board_pin, i + 14, 167 + (i * 15.5), 29, 7, 7, (0, 0, 0)))

        for i in range(0, 8):
            self.pin_power.append(Pin(board_pin, i + 24, 331 + (i * 15.5), 29, 7, 7, (0, 0, 0)))

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.power_btn.is_clicked(event.pos):
                        if self.mcu_board.board_power.is_plugged:
                            self.mcu_board.board_power.unplug_power()
                        else:
                            self.mcu_board.board_power.plug_power()

        mouse_button = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        for pin in self.pin_power:
            if pin.is_clicked(mouse_pos):
                pin.show_text()
            else:
                pin.hide_text()

        if mouse_button[0]:
            if self.reset_button.is_clicked(mouse_pos):
                self.mcu_board.reset_controller.enable_ext_reset()
        else:
            if self.reset_button.is_clicked(mouse_pos):
                self.mcu_board.reset_controller.disable_ext_reset()

    def update(self):
        pass

    def draw(self):
        self.screen.fill((200, 218, 234))

        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_render = self.font.render(
            f"X: {self.mouse_pos[0]} Y: {self.mouse_pos[1]}", True, (0, 0, 0)
        )
        self.screen.blit(self.mouse_render, (10, 10))
        self.board.draw(self.screen)
        self.reset_button.draw(self.screen)

        self.power_led.draw(self.screen)
        self.builtin_led.draw(self.screen)
        self.tx_led.draw(self.screen)
        self.rx_led.draw(self.screen)

        self.power_btn.draw(self.screen, self.font)

        for pin in self.pin_power:
            pin.draw(self.screen, self.font)

        pygame.display.flip()

    def exit(self):
        pygame.quit()
        sys.exit()
