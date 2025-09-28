import pygame
from .button import Button

class Menu():
    def __init__(self, screen, background):
        self.screen = screen
        self.bg = background
        self.game_logo = pygame.image.load('assets/menu/logos/Beat_Strike.png')
        self.game_logo_rect = self.game_logo.get_rect(center=(960, 220))

        self.buttons_name = ['jogar', 'opcoes', 'sair']
        self.selected_index = 0

        self.mouse_pos = (0, 0)

        self.load_menu_buttons()

    def load_menu_buttons(self):
        self.buttons = {}
        y = 460

        for button in self.buttons_name:
            path_off = f"assets/menu/buttons/{button}_button_no_light.png"
            img_off = pygame.image.load(path_off).convert_alpha()
            img_off = pygame.transform.scale(img_off, (318, 84))

            path_on = f"assets/menu/buttons/{button}_button_light.png"
            img_on = pygame.image.load(path_on).convert_alpha()
            img_on = pygame.transform.scale(img_on, (318, 84))

            self.buttons[button] = Button(801, y, img_off, img_on)
            y += 114

    def run(self, events, dt):
        self.mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.buttons_name)

                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.buttons_name)

                if event.key == pygame.K_RETURN:
                    selected_button = self.buttons_name[self.selected_index]
                    if selected_button == 'jogar': return 'player_select'
                    elif selected_button == 'opcoes': return 'options'
                    elif selected_button == 'sair': return 'quit'

            if self.buttons['jogar'].check_click(event): return 'player_select'
            if self.buttons['opcoes'].check_click(event): return 'options'
            elif self.buttons['sair'].check_click(event): return 'quit'

        self.bg.update(dt)

        for i, name in enumerate(self.buttons_name):
            if self.buttons[name].check_hover(self.mouse_pos):
                self.selected_index = i
                break

        for i, name in enumerate(self.buttons_name):
            button = self.buttons[name]
            if i == self.selected_index:
                button.image = button.img_on
            else:
                button.image = button.img_off

        self.bg.draw(self.screen, (0, 0))
        self.screen.blit(self.game_logo, self.game_logo_rect)

        for button in self.buttons:
            self.buttons[button].draw(self.screen)

        pygame.display.update()

        return 'menu'
