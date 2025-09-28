import pygame
from .animation import Animation
from .button import Button

class ScoreScreenBase():
    def __init__(self, screen, bg_path):
        self.screen = screen
        self.bg = Animation(bg_path)
        self.overlay_width = 700
        self.overlay_height = 400
        self.font = pygame.font.Font('assets/fonts/Super Trend.ttf', 48)
        self.selected_idx = 0
        self.mouse_pos = (0, 0)
        self.options = ['restart', 'return']

    def _init_player(self, config):
        player = {}
        player['overlay_rect'] = pygame.Rect(config['overlayx'], config['overlayy'], self.overlay_width, self.overlay_height)
        player['overlay'] = pygame.Surface((self.overlay_width, self.overlay_height), pygame.SRCALPHA)
        pygame.draw.rect(
            surface=player['overlay'],
            color=(0,0,0,120),
            rect=pygame.Rect(0,0,self.overlay_width,self.overlay_height),
            border_radius=15
        )
        spacing = 50
        player['combo_rect'] = pygame.Rect(config['textx'], config['texty'], self.overlay_width, self.overlay_height)
        player['perfect_rect'] = pygame.Rect(config['textx'], config['texty'] + spacing, self.overlay_width, self.overlay_height)
        player['good_rect'] = pygame.Rect(config['textx'], config['texty'] + spacing*2, self.overlay_width, self.overlay_height)
        player['bad_rect'] = pygame.Rect(config['textx'], config['texty'] + spacing*3, self.overlay_width, self.overlay_height)
        player['score_rect'] = pygame.Rect(config['textx'], config['texty'] + spacing*4, self.overlay_width, self.overlay_height)
        player['misses_rect'] = pygame.Rect(config['textx'], config['texty'] + spacing*5, self.overlay_width, self.overlay_height)

        return player

    def _load_buttons(self, num_player):
        restart_img = pygame.image.load('assets/menu/score_screen/restart_button.png')
        restart_img = pygame.transform.scale(restart_img, (90, 90))

        return_img = pygame.image.load('assets/menu/score_screen/return_button.png')
        return_img = pygame.transform.scale(return_img, (83, 90))

        if num_player == 1:
            self.restart_button = Button(786, 740, restart_img)
            self.return_button = Button(1043, 740, return_img)
        elif num_player == 2:
            self.restart_button = Button(786, 740, restart_img)
            self.return_button = Button(1050, 740, return_img)

    def _draw_player(self, player, score_board, score):
        self.screen.blit(player['overlay'], player['overlay_rect'].topleft)

        pygame.draw.rect(self.screen, (234, 0, 255), player['overlay_rect'], 3, border_radius=10)
        combo_text = self.font.render(f"Combo Máximo: {score_board['combo_max']}", True, (255, 255, 255))
        perfect_text = self.font.render(f"Acertos Perfeitos: {score_board['perfect']}", True, (255, 255, 255))
        good_text = self.font.render(f"Acertos Bons: {score_board['good']}", True, (255, 255, 255))
        bad_text = self.font.render(f"Acertos Ruins: {score_board['bad']}", True, (255, 255, 255))
        score_text = self.font.render(f"Pontuação: {score}", True, (255, 255, 255))
        misses_text = self.font.render(f"Erros: {score_board['misses']}", True, (255, 255, 255))

        self.screen.blit(combo_text, player['combo_rect'].topleft)
        self.screen.blit(perfect_text, player['perfect_rect'].topleft)
        self.screen.blit(good_text, player['good_rect'].topleft)
        self.screen.blit(bad_text, player['bad_rect'].topleft)
        self.screen.blit(score_text, player['score_rect'].topleft)
        self.screen.blit(misses_text, player['misses_rect'].topleft)

    def _handle_score_screen(self, events, dt):
        self.mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected_idx = (self.selected_idx + 1) % len(self.options)
                if event.key == pygame.K_LEFT:
                    self.selected_idx = (self.selected_idx - 1) % len(self.options)
                if event.key == pygame.K_RETURN:
                    if self.selected_idx == 0: return 'restart_game'
                    elif self.selected_idx == 1: return 'menu'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.restart_button.check_click(event): return 'restart_game'
                if self.return_button.check_click(event): return 'menu'
        if self.restart_button.check_hover(self.mouse_pos): self.selected_idx = 0
        if self.return_button.check_hover(self.mouse_pos): self.selected_idx = 1

        self.bg.update(dt)
        self.bg.draw(self.screen, (0, 0))
        self.restart_button.draw(self.screen)
        self.return_button.draw(self.screen)

        if self.selected_idx == 0:
            rect = self.restart_button.rect.inflate(20, 20)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=15)

        elif self.selected_idx == 1:
            rect = self.return_button.rect.inflate(20, 20)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=15)

        return None

class ScoreScreenP1(ScoreScreenBase):
    def __init__(self, screen, bg_path, score_board, score):
        super().__init__(screen, bg_path)
        config = {
            'overlayx': 610,
            'overlayy': 320,
            'textx': 630,
            'texty': 340
        }
        self.score_board = score_board
        self.score = score
        self.player = self._init_player(config)
        self._load_buttons(1)

    def run(self, events, dt):
        result = self._handle_score_screen(events, dt)
        self._draw_player(self.player, self.score_board, self.score)

        if result:
            return result

        pygame.display.update()
        return 'score_screen'

class ScoreScreenP2(ScoreScreenBase):
    def __init__(self, screen, bg_path, score_board_p1, score_p1, score_board_p2, score_p2):
        super().__init__(screen, bg_path)
        config1 = {
            'overlayx': 50,
            'overlayy': 320,
            'textx': 70,
            'texty': 340
        }
        self.player1 = self._init_player(config1)
        self.score_board1 = score_board_p1
        self.score1 = score_p1

        config2 = {
            'overlayx': 1170,
            'overlayy': 320,
            'textx': 1190,
            'texty': 340
        }
        self.player2 = self._init_player(config2)
        self.score_board2 = score_board_p2
        self.score2 = score_p2
        self._load_buttons(2)

    def run(self, events, dt):
        result = self._handle_score_screen(events, dt)
        self._draw_player(self.player1, self.score_board1, self.score1)
        self._draw_player(self.player2, self.score_board2, self.score2)

        if result:
            return result

        pygame.display.update()
        return 'score_screen'
