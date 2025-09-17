import pygame
from .animated_bg import Animatedbackground
from .button import Button

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.bg = Animatedbackground("assets/menu/background_menu")

        self.blink_timer = 0
        self.blink_interval = 500

        self.load_menu_buttons()

    def load_menu_buttons(self):
        self.buttons = {}
        botoes = ["jogar", "loja", "sair"]
        y = 360

        for botao in botoes:
            caminho_apagada = f"assets/menu/buttons/{botao}_button_no_light.png"
            img_apagada = pygame.image.load(caminho_apagada).convert_alpha()
            img_apagada = pygame.transform.scale(img_apagada, (318, 84))

            caminho_acesa = f"assets/menu/buttons/{botao}_button_light.png"
            img_acesa = pygame.image.load(caminho_acesa).convert_alpha()
            img_acesa = pygame.transform.scale(img_acesa, (318, 84))

            self.buttons[botao] = Button(801, y, img_apagada, img_acesa)
            y += 114

    def update_blinking(self, dt):
        self.blink_timer += dt
        if self.blink_timer >= self.blink_interval:
            self.blink_timer = 0
            for button in self.buttons:
                self.buttons[button].toggle_image()

    def run(self, fps):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

                if self.buttons['sair'].check_click(event):
                    return 'quit'

            self.bg.update(dt)
            self.update_blinking(dt)

            self.bg.draw(self.screen)
            for button in self.buttons:
                self.buttons[button].draw(self.screen)

            pygame.display.update()
