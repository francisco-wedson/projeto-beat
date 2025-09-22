import pygame
from .button import BackButton
from .button import Button

class BackgroundSelect:
    def __init__(self, screen, background):
        self.screen = screen
        self.bg = background

        self.backgrounds = ['sonic', 'hatsune stage', 'terrace', 'throne room']
        self.options = ['voltar', 'jogar']
        self.bgs_img = []

        self.selected_index_menu = 1
        self.selected_index_bg = 1
        self.mouse_pos = (0, 0)

        #Carregar assets
        arrow_side = pygame.image.load('assets/menu/bg_select/side_arrow.png')
        arrow_side = pygame.transform.scale(arrow_side, (60, 34))
        arrow_left = pygame.transform.rotate(arrow_side, -90)
        arrow_right = pygame.transform.flip(arrow_left, True, False)

        #Overlay
        self.overlay = pygame.Surface((1720, 600), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        #Spots
        base_size = (810, 540)
        scale_factor_side = 0.7
        side_width = int(base_size[0] * scale_factor_side)
        side_height = int(base_size[1] * scale_factor_side)
        side_size = (side_width, side_height)

        self.spots = {
            'left': {'size': side_size, 'pos': (140, 301), 'alpha': 150},
            'center': {'size': base_size, 'pos': (555, 220), 'alpha': 255},
            'right': {'size': side_size, 'pos': (1213, 301), 'alpha': 150}
        }

        #Botões
        #self.back_button = BackButton()
        self.arrow_left = Button(20, 473, arrow_left)
        self.arrow_right = Button(1840, 473, arrow_right)

        #Load Img Background
        self._load_backgrounds()

    def _change_selection(self, direction):
        new_idx = (self.selected_index_bg + direction + len(self.backgrounds)) % len(self.backgrounds)
        self.selected_index_bg = new_idx

    def _load_backgrounds(self):
        for bg in self.backgrounds:
            if bg == 'sonic' or bg == 'hatsune stage':
                bg_path = f'assets/menu/bg_select/{bg}.jpeg'
            else:
                bg_path = f'assets/menu/bg_select/{bg}.png'

            self.bgs_img.append(pygame.image.load(bg_path))

    def run(self, events, dt):
        self.mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return 'music_select'
                if event.key == pygame.K_RIGHT: self._change_selection(1)
                if event.key == pygame.K_LEFT: self._change_selection(-1)
                if event.key == pygame.K_UP: self.selected_index_menu = 0
                if event.key == pygame.K_DOWN: self.selected_index_menu = 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.arrow_right.check_click(event):
                    self._change_selection(1)
                if self.arrow_left.check_click(event):
                    self._change_selection(-1)

        self.bg.update(dt)
        self.bg.draw(self.screen, (0, 0))
        self.screen.blit(self.overlay, (100, 190))

        center_idx = self.selected_index_bg
        left_idx = (self.selected_index_bg - 1) % len(self.backgrounds)
        right_idx = (self.selected_index_bg + 1) % len(self.backgrounds)

        bg_display = [
            (left_idx, self.spots['left']),
            (right_idx, self.spots['right']),
            (center_idx, self.spots['center'])
        ]

        for bg_index, spot in bg_display:
            bg_img = self.bgs_img[bg_index]

            scaled_img = pygame.transform.scale(bg_img, spot['size'])
            scaled_img.set_alpha(spot['alpha'])

            self.screen.blit(scaled_img, spot['pos'])

        self.arrow_left.draw(self.screen)
        self.arrow_right.draw(self.screen)

        pygame.display.update()
        return 'bg_select'
