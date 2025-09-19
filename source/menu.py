import pygame
from .animated_bg import Animatedbackground
from .button import Button

class Menu():
    def __init__(self, screen, background):
        self.screen = screen
        self.bg = background

        self.buttons_name = ['jogar', 'loja', 'opcoes', 'sair']
        self.selected_index = 0

        self.mouse_pos = (0, 0)

        self.load_menu_buttons()

    def load_menu_buttons(self):
        self.buttons = {}
        y = 460

        for botao in self.buttons_name:
            caminho_apagada = f"assets/menu/buttons/{botao}_button_no_light.png"
            img_apagada = pygame.image.load(caminho_apagada).convert_alpha()
            img_apagada = pygame.transform.scale(img_apagada, (318, 84))

            caminho_acesa = f"assets/menu/buttons/{botao}_button_light.png"
            img_acesa = pygame.image.load(caminho_acesa).convert_alpha()
            img_acesa = pygame.transform.scale(img_acesa, (318, 84))

            self.buttons[botao] = Button(801, y, img_apagada, img_acesa)
            y += 114

    def run(self, events, dt):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.buttons_name)

                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.buttons_name)

                if event.key == pygame.K_RETURN:
                    selected_button = self.buttons_name[self.selected_index]
                    if selected_button == 'jogar': return 'player_select'
                    elif selected_button == 'sair': return 'quit'

            if self.buttons['jogar'].check_click(event): return 'player_select'
            elif self.buttons['sair'].check_click(event): return 'quit'

        self.bg.update(dt)

        for i, name in enumerate(self.buttons_name):
            if self.buttons[name].rect.collidepoint(self.mouse_pos):
                self.selected_index = i
                break

        for i, name in enumerate(self.buttons_name):
            button = self.buttons[name]
            if i == self.selected_index:
                button.image = button.img_acesa
            else:
                button.image = button.img_apagada

        self.bg.draw(self.screen)

        for button in self.buttons:
            self.buttons[button].draw(self.screen)

        pygame.display.update()

        return 'menu'
