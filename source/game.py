import pygame
from .renderer import Template, Note
from .animation import Animation
from .button import Button
import os
import json

class GameBase():
    def __init__(self, screen, game_context, config):
        self.screen = screen
        self.game_context = game_context
        self.config = config
        self.first_note_spawned = False
        pygame.mixer.music.stop()
        self.bg = Animation(self.game_context['bg_path'])
        self.overlay_size = (570, 1050)
        self.overlay = pygame.Surface(self.overlay_size, pygame.SRCALPHA)
        self.animations_name = ['idle', 'left', 'right', 'up', 'down', 'miss', 'dying']
        self.anim_idx = {
                0: 'left',
                1: 'up',
                2: 'down',
                3: 'right'
            }
        self.mouse_pos = (0, 0)

        self.font_score = pygame.font.Font('assets/fonts/Super Trend.ttf', 32)
        self.font_hit = pygame.font.Font('assets/fonts/m23.TTF', 22)
        self.font_0 = pygame.font.Font('assets/fonts/Autumn Crush.ttf', 46)
        self.font_10 = pygame.font.Font('assets/fonts/Bigbesty.ttf', 46)
        self.font_25 = pygame.font.Font('assets/fonts/The Melody.otf', 40)
        self.font_40 = pygame.font.Font('assets/fonts/HauntedHillRough-Rough.ttf', 50)
        self.font_60 = pygame.font.Font('assets/fonts/Bing Bam Boum.ttf', 40)

        self.miss_text = self.font_hit.render('Errou', True, (255, 49, 49))
        self.perfect_text = self.font_hit.render('Perfeito', True, (207, 255, 4))
        self.good_text = self.font_hit.render('Bom', True, (31, 81, 255))
        self.bad_text = self.font_hit.render('Ruim', True, (57, 255, 20))

        self.combo_thresholds = [
            (10, "Boa!", self.font_10, 1.5),
            (25, "Isso aí!", self.font_25, 2),
            (40, "Brabo!", self.font_40, 3),
            (60, "Insano!", self.font_60, 4),
        ]

    def _init_player(self, config):
        # -lane_x, lane_keys, overlay_rect
        player = {}
        player['lane_x'] = config['lane_x']
        player['template'] = [Template(x, 70) for x in config['lane_x']]
        player['notes'] = pygame.sprite.Group()
        player['lane_keys'] = config['lane_keys']
        player['score'] = 0
        player['score_board'] = {'hits':0, 'perfect':0, 'good':0, 'bad':0, 'misses':0, 'combo_max': 0}
        player['overlay_size'] = config.get('overlay_size', (570,1050))
        player['overlay_rect'] = config.get('overlay_rect', (675,30))
        player['overlay'] = pygame.Surface(player['overlay_size'], pygame.SRCALPHA)
        pygame.draw.rect(
            surface=player['overlay'],
            color=(0,0,0,120),
            rect=pygame.Rect(0,0,player['overlay_size'][0],player['overlay_size'][1]),
            border_radius=15
        )
        player['char_rect'] = config['char_rect']
        player['anim'] = {}
        for anim_name in self.animations_name:
            char_animation_path = f'assets/characters_animation/{config['character']}/{anim_name}'
            loop = False if anim_name == 'dying' else True
            player['anim'][anim_name] = Animation(char_animation_path, speed=20, loop=loop, flip=config['flip'])
        player['actual_anim'] = player['anim']['idle']
        player['char_alive'] = True
        player['hold_effects'] = {
            0: False,
            1: False,
            2: False,
            3: False
        }
        player['hold_anims'] = {}
        player['hit_effects'] = []
        for i, lane_x in enumerate(player['lane_x']):
            player['hold_effects'][i] = False
            player['hold_anims'][i] = Animation("assets/effects_animation/lightning_holding", speed=15, loop=True)
        player['score_text'] = self.font_score.render(f'Pontuação: {player['score']}', True, '#FFFFFF')
        player['score_text_rect'] = player['score_text'].get_rect(center=(config['score_rect'][0], config['score_rect'][1]))
        player['hit_texts'] = []
        player['combo'] = 0
        player['combo_info'] = {
            'current_multiplier': 1,
            'threshold_msg': None,
            'current_font': self.font_0,
            'combo_rect': config['combo_rect']
        }
        player['combo_texts'] = []
        player['current_idx'] = 0
        return player

    def _keys_to_pygame(self, keybinds_player):
        order = ['left', 'down', 'up', 'right']
        pygame_keys = {}
        for idx, k in enumerate(order):
            key_str = keybinds_player.get(k, "")
            keycode = None

            keycode = pygame.key.key_code(key_str)
            pygame_keys[idx] = keycode
        return pygame_keys

    def _spawn_note(self, player, lane, duration):
        if not self.first_note_spawned:
            self.first_note_spawned = True
        x = player['lane_x'][lane]
        player['notes'].add(Note(x, lane, duration))

    def _handle_input_player(self, player, event):
        hit_now = False
        for lane, key in player['lane_keys'].items():
            if event.key == key:
                target_lane = lane
                break

        if event.type == pygame.KEYDOWN and event.key in player['lane_keys'].values():
            for note in player['notes']:
                if note.lane == target_lane and pygame.sprite.collide_rect(note, player['template'][lane]):
                    hit_now = True
                    player['score_board']['hits'] += 1
                    player['combo'] += 1

                    if player['combo'] >= player['score_board']['combo_max']:
                        player['score_board']['combo_max'] = player['combo']

                    combo_surface = player['combo_info']['current_font'].render(f"x{player['combo']}", True, (255, 230, 0))
                    combo_rect = combo_surface.get_rect(topleft=(player['combo_info']['combo_rect']))

                    player['combo_texts'].append({
                        'surface': combo_surface,
                        'rect': combo_rect,
                        'start': pygame.time.get_ticks(),
                        'duration': 500,
                    })

                    for limit, message, font, mult in self.combo_thresholds:
                        if player['combo'] == limit:
                            player['combo_info']['current_multiplier'] = mult
                            player['combo_info']['current_font'] = font
                            text_surface = font.render(message, True, (255, 255, 0))
                            text_rect = text_surface.get_rect(topleft=(player['combo_info']['combo_rect'][0],
                                                                       player['combo_info']['combo_rect'][1] + 60))
                            player['combo_texts'].append({
                                'surface': text_surface,
                                'rect': text_rect,
                                'start': pygame.time.get_ticks(),
                                'duration': 500,
                            })
                    if note.duration > 0:
                        player['hold_effects'][target_lane] = True
                        note.start_hold()
                        break
                    else:
                        player['hit_texts'].append({
                            'pos': (player['template'][target_lane].rect.right + 10, player['template'][target_lane].rect.top),
                            'start_time': pygame.time.get_ticks(),
                            'duration': 1000
                        })
                        player['hit_effects'].append({
                            'lane': target_lane,
                            'timer': 500,
                            'anim': Animation('assets/effects_animation/explosion', (200, 200), speed=20, loop=False)
                        })

                        dist = abs(note.rect.centery - player['template'][target_lane].rect.centery)
                        if dist <= 10:
                            player['score_board']['perfect'] += 1
                            player['hit_texts'][-1]['surface'] = self.perfect_text
                            player['score'] += int(200 * player['combo_info']['current_multiplier'])
                        elif dist <= 25:
                            player['score_board']['good'] += 1
                            player['hit_texts'][-1]['surface'] = self.good_text
                            player['score'] += int(100 * player['combo_info']['current_multiplier'])
                        else:
                            player['score_board']['bad'] += 1
                            player['hit_texts'][-1]['surface'] = self.bad_text
                            player['score'] += int(50 * player['combo_info']['current_multiplier'])
                        note.kill()
                        break
            if not hit_now and self.first_note_spawned:
                player['score_board']['misses'] += 1
                player['combo'] = 0
                player['current_multiplier'] = 1
                player['combo_info']['current_font'] = self.font_0
                player['actual_anim'] = player['anim']['miss']
                player['char_alive'] = True
                player['hit_texts'].append({
                    'surface': self.miss_text,
                    'pos': (player['template'][target_lane].rect.right + 10, player['template'][target_lane].rect.top),
                    'start_time': pygame.time.get_ticks(),
                    'duration': 1000
                })

            if player['score_board']['misses'] > player['score_board']['hits']:
                player['actual_anim'] = player['anim']['dying']
                player['char_alive'] = False
            elif hit_now:
                player['actual_anim'] = player['anim'][self.anim_idx[target_lane]]
                player['char_alive'] = True

        if event.type == pygame.KEYUP and event.key in player['lane_keys'].values():
            for note in player['notes']:
                if note.lane == target_lane and note.is_holding:
                    player['hit_texts'].append({
                        'pos': (player['template'][target_lane].rect.right + 10, player['template'][target_lane].rect.top),
                        'start_time': pygame.time.get_ticks(),
                        'duration': 1000
                    })
                    hold_ratio = min((note.hold_time / note.duration) * 100, 100.0)
                    if hold_ratio > 95:
                        player['score_board']['perfect'] += 1
                        player['hit_texts'][-1]['surface'] = self.perfect_text
                        player['score'] += int(300 * player['combo_info']['current_multiplier'])
                    elif hold_ratio >= 65:
                        player['score_board']['good'] += 1
                        player['hit_texts'][-1]['surface'] = self.good_text
                        player['score'] += int(200 * player['combo_info']['current_multiplier'])
                    else:
                        player['score_board']['bad'] += 1
                        player['hit_texts'][-1]['surface'] = self.bad_text
                        player['score'] += int(100 * player['combo_info']['current_multiplier'])
                    note.stop_hold()
                    break
            if target_lane in player['hold_effects']:
                player['hold_effects'][target_lane] = False

    def _update_player(self, player, keys, dt):
        player['notes'].update(dt)

        for note in list(player['notes']):
            if note.rect.bottom < 70 and not note.missed and not note.hold_failed:
                note.missed = True
                player['score_board']['misses'] += 1
                player['combo'] = 0
                player['current_multiplier'] = 1
                player['combo_info']['current_font'] = self.font_0
                player['hit_texts'].append({
                    'surface': self.miss_text,
                    'pos': (player['template'][note.lane].rect.right + 10, player['template'][note.lane].rect.top),
                    'start_time': pygame.time.get_ticks(),
                    'duration': 1000
                })
                if note.duration == 0:
                    note.kill()

                else:
                    note.hold_failed = True

                if player['score_board']['misses'] > player['score_board']['hits']:
                    player['actual_anim'] = player['anim']['dying']
                    player['char_alive'] = False
                else:
                    player['actual_anim'] = player['anim']['miss']
                    player['char_alive'] = True

        for note in list(player['notes']):
            if note.duration > 0 and note.hold_time >= note.duration:
                player['hit_texts'].append({
                    'pos': (player['template'][note.lane].rect.right + 10, player['template'][note.lane].rect.top),
                    'start_time': pygame.time.get_ticks(),
                    'duration': 1000
                })
                hold_ratio = min((note.hold_time / note.duration) * 100, 100.0)
                if hold_ratio >= 95:
                    player['score_board']['perfect'] += 1
                    player['hit_texts'][-1]['surface'] = self.perfect_text
                    player['score'] += int(300 * player['combo_info']['current_multiplier'])
                elif hold_ratio >= 65:
                    player['score_board']['good'] += 1
                    player['hit_texts'][-1]['surface'] = self.good_text
                    player['score'] += int(200 * player['combo_info']['current_multiplier'])
                else:
                    player['score_board']['bad'] += 1
                    player['hit_texts'][-1]['surface'] = self.bad_text
                    player['score'] += int(100 * player['combo_info']['current_multiplier'])
                player['combo'] += 1
                player['hold_effects'][note.lane] = False
                note.kill()
            if note.duration > 0:
                tail_bottom = note.rect.bottom + note.current_tail_height
                if tail_bottom <= 0:
                    note.kill()

        if player['char_alive'] == True:
            player['anim']['dying'].reset()

        player['actual_anim'].update(dt)

        for i, template in enumerate(player['template']):
            template.update_visuals(keys[player['lane_keys'][i]])

        for effect in list(player['hit_effects']):
            effect['timer'] -= dt
            effect['anim'].update(dt)
            if effect['timer'] <= 0:
                player['hit_effects'].remove(effect)

        for i, anim in player['hold_anims'].items():
            if player['hold_effects'][i]:
                anim.update(dt)

        player['score_text'] = self.font_score.render(f'Pontuação: {player['score']}', True, '#FFFFFF')
        current_time = pygame.time.get_ticks()
        for text in player['combo_texts']:
            if current_time - text['start'] > text['duration']:
                player['combo_texts'].remove(text)

    def _draw_player(self, player):
        self.screen.blit(player['overlay'], player['overlay_rect'])
        self.screen.blit(player['score_text'], player['score_text_rect'])

        for effect in player['hit_effects']:
            center_pos = player['template'][effect['lane']].rect.center
            effect_image = effect['anim'].image
            effect['anim'].draw(self.screen, (center_pos), True)

        player['actual_anim'].draw(self.screen, player['char_rect'], True)
        for template in player['template']:
            template.draw(self.screen)
        for note in player['notes']:
            note.draw(self.screen)

        for i, active in player['hold_effects'].items():
            if active:
                hold_rect = player['template'][i].rect.midbottom
                player['hold_anims'][i].draw(self.screen, (hold_rect[0] - 5, hold_rect[1] - 20), True)

        current_time = pygame.time.get_ticks()
        for t in player['hit_texts'][:]:
            if current_time - t['start_time'] > t['duration']:
                player['hit_texts'].remove(t)
            else:
                self.screen.blit(t['surface'], t['pos'])

        for text in player['combo_texts']:
            self.screen.blit(text['surface'], text['rect'])

    def _update_notes_spawn(self, player, chart, current_time):
        while player['current_idx'] < len(chart):
            note_info = chart[player['current_idx']]
            if current_time >= note_info['time_start']:
                self._spawn_note(player, note_info['lane'], note_info['duration'])
                player['current_idx'] += 1
            else:
                break

class GameP1(GameBase):
    def __init__(self, screen, game_context, config):
        super().__init__(screen, game_context, config)
        lane_keys = self._keys_to_pygame(self.config['keybinds']['player1'])
        P1_CONFIG = {
            'lane_x': [805, 935, 1065, 1195],
            'lane_keys': lane_keys,
            'overlay_rect': (775, 30),
            'char_rect': (410, 540),
            'score_rect': (430, 260),
            'flip': False,
            'character': game_context['characters'][1],
            'combo_rect': (670, 70)
        }
        self.player = self._init_player(P1_CONFIG)
        music = game_context['music']
        chart_path = f'assets/music/game/{music}/{music}.json'
        with open(chart_path, 'r') as f:
            self.chart = json.load(f)
        self.music_path = f'assets/music/game/{music}/{music}.ogg'
        self.is_music_playing = False

    def run(self, events, dt):
        pygame.mouse.set_visible(False)
        if not self.is_music_playing:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(self.config['volume']['game'])
            pygame.mixer.music.play()
            self.is_music_playing = True

        current_time = pygame.mixer.music.get_pos() / 1000.0
        self._update_notes_spawn(self.player, self.chart, current_time)

        if not pygame.mixer.music.get_busy() and self.is_music_playing:
            pygame.mixer.music.stop()
            return 'score_screen', self.player['score_board'], self.player['score']

        keys = pygame.key.get_pressed()
        self._update_player(self.player, keys, dt)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return 'menu'
                if event.key == pygame.K_F5:
                    pygame.mixer.music.stop()
                    return 'restart_game'
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP and event.key in self.player['lane_keys'].values():
                self._handle_input_player(self.player, event)

        self.bg.update(dt)
        self.bg.draw(self.screen, (0,0))
        self._draw_player(self.player)

        pygame.display.update()
        return 'game'

class GameP2(GameBase):
    def __init__(self, screen, game_context, config):
        super().__init__(screen, game_context, config)
        lane_keys_p1 = self._keys_to_pygame(config['keybinds']['player1'])
        lane_keys_p2 = self._keys_to_pygame(config['keybinds']['player2'])
        P1_CONFIG = {
            'lane_x': [50, 180, 310, 440],
            'lane_keys': lane_keys_p1,
            'overlay_rect': (30, 30),
            'char_rect': (820, 540),
            'score_rect': (840, 260),
            'flip': True,
            'character': game_context['characters'][1],
            'combo_rect': (675, 70)
        }
        P2_CONFIG = {
            'lane_x': [1349, 1479, 1609, 1739],
            'lane_keys': lane_keys_p2,
            'overlay_rect': (1329, 30),
            'char_rect': (1100, 540),
            'score_rect': (1120, 260),
            'flip': False,
            'character': game_context['characters'][2],
            'combo_rect': (1234, 70)
        }
        self.player_1 = self._init_player(P1_CONFIG)
        self.player_2 = self._init_player(P2_CONFIG)
        music = game_context['music']
        chart_path = f'assets/music/game/{music}/{music}.json'
        with open(chart_path, 'r') as f:
            self.chart = json.load(f)
        self.music_path = f'assets/music/game/{music}/{music}.ogg'
        self.is_music_playing = False

    def run(self, events, dt):
        pygame.mouse.set_visible(False)
        if not self.is_music_playing:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(self.config['volume']['game'])
            pygame.mixer.music.play()
            self.is_music_playing = True

        current_time = pygame.mixer.music.get_pos() / 1000.0
        self._update_notes_spawn(self.player_1, self.chart, current_time)
        self._update_notes_spawn(self.player_2, self.chart, current_time)

        if not pygame.mixer.music.get_busy() and self.is_music_playing:
            pygame.mixer.music.stop()
            return 'score_screen', self.player_1['score_board'], self.player_1['score'], self.player_2['score_board'], self.player_2['score']

        keys = pygame.key.get_pressed()
        self._update_player(self.player_1, keys, dt)
        self._update_player(self.player_2, keys, dt)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return 'menu'
                if event.key == pygame.K_F5:
                    pygame.mixer.music.stop()
                    return 'restart_game'
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP and event.key in self.player_1['lane_keys'].values():
                self._handle_input_player(self.player_1, event)

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP and event.key in self.player_2['lane_keys'].values():
                self._handle_input_player(self.player_2, event)

        self.bg.update(dt)
        self.bg.draw(self.screen, (0,0))
        self._draw_player(self.player_1)
        self._draw_player(self.player_2)

        pygame.display.update()
        return 'game'
