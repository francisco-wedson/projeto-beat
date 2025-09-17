import pygame
from pygame.locals import *
from .renderer import Molde
from .renderer import Nota
import os
import json

class Game():
    def __init__(self, screen, lagura, altura):
        self.screen = screen
        self.acertos = 0
        #Tecla
        self.moldes = [Molde(390, 70), Molde(490, 70), Molde(590, 70), Molde(690, 70)]
        self.notas = pygame.sprite.Group()
        chart_path = os.path.join('assets', 'musicas', 'Its-Going-Down-Now.json') # Use o nome do .json que você gerou
        with open(chart_path, 'r') as f:
            self.chart = json.load(f)
 
        #batidas
        self.current_idx = 0
        self.start_time = None

        #Lanes para teclas
        self.lane_keys = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
        self.lane_x = [390, 490, 590, 690]

    def draw_text(self, texto, fonte, cor, x, y):
        msg = fonte.render(texto, True, cor)
        self.screen.blit(msg, (x, y))

    def spawn_nota(self, x, tecla):
        self.notas.add(Nota(x, 1080, tecla))

    def update(self):
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()

        current_time = (pygame.time.get_ticks() - self.start_time) / 1000.0

        if self.current_idx < len(self.chart):
            onset_time, lane = self.chart[self.current_idx]
            if current_time >= onset_time:
                self.spawn_nota(self.lane_x[lane], self.lane_keys[lane])
                self.current_idx += 1

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

    def run(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.load('assets/musicas/Its-Going-Down-Now-fixed.wav')
        pygame.mixer.music.play()

        while True:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

            self.update()
            self.screen.fill((0,0,0))
            self.draw()
            pygame.display.update()

        return 'menu'
