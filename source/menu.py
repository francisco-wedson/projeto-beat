import pygame
from .animated_bg import Animatedbackground
from .button import Button

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.bg = Animatedbackground("assets/menu/background_menu")

        #Botões
        #self.load_buttons()
        #self.calculate_buttons_positions()
        #self.create_buttons_objects()

    def load_buttons(self):
        play_img = pygame.image.load("assets/menu/buttons/play.jpg").convert_alpha()

    def run(self, fps):
        clock = pygame.time.Clock()
        while True:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

            self.bg.update(clock.get_time())
            self.bg.draw(self.screen)

            pygame.display.update()
