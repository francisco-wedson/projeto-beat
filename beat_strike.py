import pygame
from pygame.locals import *
from sys import exit
from source.game import Game
from source.menu import Menu
from source.animation import Animation
from source.player_select import PlayerSelect
from source.char_select import CharSelect

pygame.init()
pygame.mixer.init()

#Nome da janela
pygame.display.set_caption("Beat Strike")

#Tela
screen_size = (1920, 1080)

resolucao_monitor = screen_size
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

animated_bg = Animation("assets/menu/background_menu", screen_size)

#FPS
fps = 60

#Estado atual
state = 'menu'
clock = pygame.time.Clock()
fps = 60

game_context = {
    'players': 1
}

#Menu
screens = {
    'menu': Menu(screen, animated_bg),
    'player_select': PlayerSelect(screen, animated_bg),
}

while True:
    dt = clock.tick(fps)
    events = pygame.event.get()

    for event in events:
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

    if state == 'menu':
        state = screens['menu'].run(events, dt)

    elif state == 'player_select':
        result = screens['player_select'].run(events, dt)

        if isinstance(result, tuple):
            state = result[0]
            game_context['players'] = result[1]

            screens['char_select'] = CharSelect(screen, animated_bg, game_context['players'])

        else:
            state = result

    elif state == 'char_select':
        result = screens['char_select'].run(events, dt)

        if isinstance(result, tuple):
            state = result[0]
            game_context['character'] = result[1]

        else:
            state = result

    elif state == 'game':
        pygame.mixer.music.stop()

        game = Game(screen, game_context)
        state = game.run()

        if state == 'menu':
            pygame.mixer.music.play(-1)

    elif state == 'quit':
        pygame.quit()
        exit()
