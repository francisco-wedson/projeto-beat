import pygame
from pygame.locals import *
from sys import exit
from source.game import Game
from source.menu import Menu

pygame.init()

#Nome da janela
pygame.display.set_caption("Beat Strike")

#Tela
largura, altura = 1920, 1080

info = pygame.display.Info()
resolucao_monitor = (info.current_w, info.current_h)
screen = pygame.display.set_mode(resolucao_monitor, pygame.SCALED)

#Evitar tela preta
bg = pygame.image.load('assets/menu/background_menu/frame_00_delay-0.1s.png')
bg = pygame.transform.scale(bg, resolucao_monitor)
screen.blit(bg, (0,0))
pygame.display.update()

#FPS
fps = 60

#Game
game = Game(screen, largura, altura)

#Menu
menu = Menu(screen)

#Estado atual
state = 'menu'

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

    if state == 'menu':
        state = menu.run(fps)

    elif state == 'game':
        state = game.run()

    elif state == 'quit':
        pygame.quit()
        exit()

    #game.update()
    #game.draw()
