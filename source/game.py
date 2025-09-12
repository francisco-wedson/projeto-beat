import pygame
from pygame.locals import *
from .renderer import Molde
from .renderer import Nota

pygame.init()

class Game():
    def __init__(self, screen, lagura, altura):
        self.screen = screen
        self.acertos = 0
        #Tecla
        self.moldes = [Molde(390, 70), Molde(490, 70), Molde(590, 70), Molde(690, 70)]
        self.notas = pygame.sprite.Group()

    def draw_text(self, texto, fonte, cor, x, y):
        msg = fonte.render(texto, True, cor)
        self.screen.blit(msg, (x, y))

    def spawn_nota(self, x, tecla):
        self.notas.add(Nota(x, 0, tecla))

    def update(self):
        self.notas.update()

        keys = pygame.key.get_pressed()
        for nota in self.notas:
            for molde in self.moldes:
                if pygame.sprite.collide_rect(nota, molde):
                    if keys[nota.tecla]:
                        self.acertos += 1
                        nota.kill()

            if nota.off_screen(self.screen.get_height()):
                nota.kill()

    def draw(self):
        for molde in self.moldes:
            molde.draw(self.screen)
        self.notas.draw(self.screen)
