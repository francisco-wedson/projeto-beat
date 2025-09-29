import pygame
from pygame.locals import *
from sys import exit
import json
import os
from source.game import GameP1, GameP2
from source.menu import Menu
from source.options import OptionsMenu
from source.animation import Animation
from source.player_select import PlayerSelect
from source.char_select import CharSelect
from source.music_select import MusicSelect
from source.bg_select import BackgroundSelect
from source.fade_out import FadeOut
from source.score_screen import ScoreScreenP1, ScoreScreenP2

pygame.init()
pygame.mixer.init()

#Nome da janela
pygame.display.set_caption("Beat Strike")

#Tela
screen_size = (1920, 1080)

resolucao_monitor = screen_size
screen = pygame.display.set_mode(resolucao_monitor, pygame.SCALED)
pygame.event.get()
pygame.mouse.set_pos(resolucao_monitor[0] // 2, resolucao_monitor[1] // 2)
pygame.event.clear()

#Carregar Configs
CONFIG_PATH = "assets/config/config.json"

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
else:
    config = {
        "volume": {"menu": 0.2, "game": 0.4},
        "keybinds": {
            "player1": {"left": "a", "down": "s", "up": "w", "right": "d"},
            "player2": {"left": "left", "down": "down", "up": "up", "right": "right"},
        },
    }

#Evitar tela preta
company_img = pygame.image.load('assets/menu/logos/Smash_Lemon.png')
company_rect = company_img.get_rect(center=screen.get_rect().center)
screen.fill((0, 0, 0))
screen.blit(company_img, company_rect)
pygame.display.update()

#Música
pygame.mixer.music.load('assets/music/menu/LupusNocte-Arcadewave.ogg')
pygame.mixer.music.set_volume(config['volume']['menu'])
pygame.mixer.music.play(-1)

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
    'options': OptionsMenu(screen, animated_bg, config),
    'player_select': PlayerSelect(screen, animated_bg),
    'music_select': MusicSelect(screen, animated_bg),
    'bg_select': BackgroundSelect(screen, animated_bg)
}

while True:
    dt = clock.tick(fps)
    events = pygame.event.get()

    pygame.mixer.music.set_volume(config['volume']['menu'])

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

    elif state == 'options':
        state = screens['options'].run(events, dt)

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
                screens['game'] = GameP1(screen, game_context, config)
            elif game_context['players'] == 2:
                screens['game'] = GameP2(screen, game_context, config)

        else:
            state = result

    elif state == 'game':
        result = screens['game'].run(events, dt)

        if result != 'game':
            pygame.mouse.set_visible(True)

        if result == 'menu':
            pygame.mixer.music.load('assets/music/menu/LupusNocte-Arcadewave.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.1)

        if isinstance(result, tuple):
            state = result[0]

            if game_context['players'] == 1:
                screens['score_screen'] = ScoreScreenP1(screen, game_context['bg_path'], result[1], result[2])
            elif game_context['players'] == 2:
                screens['score_screen'] = ScoreScreenP2(screen, game_context['bg_path'], result[1], result[2], result[3], result[4])
        else:
            state = result

    elif state == 'restart_game':
        if game_context['players'] == 1:
            screens['game'] = GameP1(screen, game_context, config)
        elif game_context['players'] == 2:
            screens['game'] = GameP2(screen, game_context, config)
        state = 'game'

    elif state == 'score_screen':
        pygame.mouse.set_visible(True)
        state = screens['score_screen'].run(events, dt)

        if state == 'menu':
            pygame.mixer.music.load('assets/music/menu/LupusNocte-Arcadewave.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.1)

    elif state == 'quit':
        pygame.quit()
        exit()
