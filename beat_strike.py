import pygame
from pygame.locals import *
from sys import exit
from source.game import Game
from source.menu import Menu
from source.animated_bg import Animatedbackground
from source.player_select import Player_select

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=8192)

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

#Música
pygame.mixer.music.load('assets/musicas/LupusNocte-Arcadewave.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

animated_bg = Animatedbackground("assets/menu/background_menu")

#FPS
fps = 60

#Menu
menu = Menu(screen, animated_bg)

#Player_select
player_select = Player_select(screen, animated_bg)

#Estado atual
state = 'menu'
clock = pygame.time.Clock()
fps = 60

game_context = {}

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

    if state == 'menu':
        dt = clock.tick(fps)
        state = menu.run(events, dt)

    elif state == 'player_select':
        dt = clock.tick(fps)
        state = player_select.run(events, dt)

    elif state == 'game':
        pygame.mixer.music.stop()

        game = Game(screen, game_context)
        state = game.run()

        if state == 'menu':
            pygame.mixer.music.play(-1)

    elif state == 'quit':
        pygame.quit()
        exit()
