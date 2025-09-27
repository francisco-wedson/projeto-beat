import pygame
from pygame.locals import *
from sys import exit
from source.game import GameP1, GameP2
from source.menu import Menu
from source.animation import Animation
from source.player_select import PlayerSelect
from source.char_select import CharSelect
from source.music_select import MusicSelect
from source.bg_select import BackgroundSelect
from source.fade_out import FadeOut

pygame.init()
pygame.mixer.init()

#Nome da janela
pygame.display.set_caption("Beat Strike")

#Tela
screen_size = (1920, 1080)

resolucao_monitor = screen_size
screen = pygame.display.set_mode(resolucao_monitor, pygame.SCALED)

#Evitar tela preta
company_img = pygame.image.load('assets/menu/logos/Smash_Lemon.png')
company_rect = company_img.get_rect(center=screen.get_rect().center)
screen.fill((0, 0, 0))
screen.blit(company_img, company_rect)
pygame.display.update()

#Música
pygame.mixer.music.load('assets/music/menu/LupusNocte-Arcadewave.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

animated_bg = Animation("assets/menu/background_menu", screen_size)

#FPS
fps = 60

#Estado atual
state = 'fade_out'
clock = pygame.time.Clock()
fps = 60

game_context = {}

#Menu
screens = {
    'fade_out': FadeOut(screen, company_img, company_rect),
    'menu': Menu(screen, animated_bg),
    'player_select': PlayerSelect(screen, animated_bg),
    'music_select': MusicSelect(screen, animated_bg),
    'bg_select': BackgroundSelect(screen, animated_bg)
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

    if state == 'fade_out':
        state = screens['fade_out'].run(events, dt)

    elif state == 'menu':
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
            game_context['characters'] = result[1]

        else:
            state = result

    elif state == 'music_select':
        result = screens['music_select'].run(events, dt)

        if isinstance(result, tuple):
            state = result[0]
            game_context['music'] = result[1]

        else:
            state = result
            screens['char_select'] = CharSelect(screen, animated_bg, game_context['players'])

    elif state == 'bg_select':
        result = screens['bg_select'].run(events, dt)

        if isinstance(result, tuple):
            state = result[0]
            game_context['bg_path'] = result[1]

            if game_context['players'] == 1:
                screens['game'] = GameP1(screen, game_context)
            elif game_context['players'] == 2:
                screens['game'] = GameP2(screen, game_context)

        else:
            state = result

    elif state == 'game':
        pygame.mouse.set_visible(False)
        state = screens['game'].run(events, dt)

        if state == 'menu':
            pygame.mixer.music.load('assets/music/menu/LupusNocte-Arcadewave.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.1)
        if state != 'game':
            pygame.mouse.set_visible(True)

    elif state == 'quit':
        pygame.quit()
        exit()
