import pygame
from .button import BackButton
from .button import Button
from .animation import Animation

class BackgroundSelect:
    def __init__(self, screen, background):
        self.screen = screen
        self.bg = background

        self.backgrounds = ['blue city', 'girl', 'hell', 'rpg', 'ranni']
        self.options = ['voltar', 'jogar']
        self.bgs_dict = {}

        self.selected_index_menu = 1
        self.selected_index_bg = 0
        self.mouse_pos = (0, 0)

        #Carregar assets
        arrow_side = pygame.image.load('assets/menu/bg_select/side_arrow.png')
        arrow_side = pygame.transform.scale(arrow_side, (60, 34))
        arrow_left = pygame.transform.rotate(arrow_side, -90)
        arrow_right = pygame.transform.flip(arrow_left, True, False)

        arrow_side_light = pygame.image.load('assets/menu/bg_select/side_arrow_light.png')
        arrow_side_light = pygame.transform.scale(arrow_side_light, (60, 34))
        arrow_left_light = pygame.transform.rotate(arrow_side_light, -90)
        arrow_right_light = pygame.transform.flip(arrow_left_light, True, False)

        play_img = pygame.image.load('assets/menu/bg_select/jogar_button_no_light.png')
        play_img = pygame.transform.scale(play_img, (318, 84))
        play_img_light = pygame.image.load('assets/menu/bg_select/jogar_button_light.png')
        play_img_light = pygame.transform.scale(play_img_light, (318, 84))

        #Overlay
        self.overlay_size = (1720, 600)
        self.overlay = pygame.Surface(self.overlay_size, pygame.SRCALPHA)
        self.overlay_rect = self.overlay.get_rect(topleft=(100, 190))
        pygame.draw.rect(
            surface=self.overlay,
            color=(0, 0, 0, 180),
            rect=pygame.Rect(0, 0, self.overlay_size[0], self.overlay_size[1]),
            border_radius=15
        )

        #Spots
        self.base_size = (720, 480)
        side_size = int(self.base_size[0] * 0.6), int(self.base_size[1] * 0.6)
        screen_center_x = self.screen.get_width() / 2
        screen_center_y = 190 + (600 / 2)
        spacing_x = 620

        self.spots = {
            'left': {'size': side_size, 'pos': (screen_center_x - spacing_x, screen_center_y), 'alpha': 180},
            'center': {'pos': (screen_center_x, screen_center_y), 'alpha': 255},
            'right': {'size': side_size, 'pos': (screen_center_x + spacing_x, screen_center_y), 'alpha': 180}
        }

        #Botões
        self.back_button = BackButton(120, 210)
        self.play_button = Button(screen_center_x, 790, play_img, play_img_light, True)
        self.arrow_left_button = Button(47, 490, arrow_left, arrow_left_light)
        self.arrow_right_button = Button(1840, 490, arrow_right, arrow_right_light)

        #Load Img Background
        self._load_backgrounds()

    def _change_selection(self, direction):
        new_idx = (self.selected_index_bg + direction + len(self.backgrounds)) % len(self.backgrounds)
        self.selected_index_bg = new_idx

    def _load_backgrounds(self):
        for bg in self.backgrounds:
            self.bgs_dict[bg] = {}
            bg_path = f'assets/backgrounds/{bg}'
            self.bgs_dict[bg]['bg_path'] = bg_path
            self.bgs_dict[bg]['bg'] = Animation(bg_path, self.base_size)

    def run(self, events, dt):
        self.mouse_pos = pygame.mouse.get_pos()

        selected_bg_name = self.backgrounds[self.selected_index_bg]

        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return 'music_select'
                if event.key == pygame.K_RIGHT: self._change_selection(1)
                if event.key == pygame.K_LEFT: self._change_selection(-1)
                if event.key == pygame.K_UP: self.selected_index_menu = 0
                if event.key == pygame.K_DOWN: self.selected_index_menu = 1

                if event.key == pygame.K_RETURN:
                    if self.selected_index_menu == 1:
                        return 'game', self.bgs_dict[selected_bg_name]['bg_path']
                    else: return 'music_select'

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.check_click(event): return 'music_select'
                if self.play_button.check_click(event):
                    return 'game', self.bgs_dict[selected_bg_name]['bg_path']
                if self.arrow_left_button.check_click(event):
                    self._change_selection(-1)
                if self.arrow_right_button.check_click(event):
                    self._change_selection(1)

        if self.back_button.check_hover(self.mouse_pos):
            self.selected_index_menu = 0
        if self.play_button.check_hover(self.mouse_pos):
            self.selected_index_menu = 1
        if self.arrow_left_button.check_hover(self.mouse_pos):
            self.arrow_left_button.image = self.arrow_left_button.img_on
        else:
            self.arrow_left_button.image = self.arrow_left_button.img_off
        if self.arrow_right_button.check_hover(self.mouse_pos):
            self.arrow_right_button.image = self.arrow_right_button.img_on
        else:
            self.arrow_right_button.image = self.arrow_right_button.img_off

        self.bg.update(dt)
        self.bg.draw(self.screen, (0, 0))
        self.screen.blit(self.overlay, self.overlay_rect)
        pygame.draw.rect(self.screen, (0, 238, 255), self.overlay_rect, 3, border_radius=15)

        left_name = self.backgrounds[(self.selected_index_bg - 1) % len(self.backgrounds)]
        right_name = self.backgrounds[(self.selected_index_bg + 1) % len(self.backgrounds)]

        bg_display = [
            (left_name, self.spots['left']),
            (right_name, self.spots['right']),
            (selected_bg_name, self.spots['center'])
        ]

        for bg_name, spot in bg_display:
            if spot == self.spots['center']:
                self.bgs_dict[bg_name]['bg'].draw(self.screen, spot['pos'], True)
                self.bgs_dict[bg_name]['bg'].update(dt)

            else:
                scaled_img = pygame.transform.scale(self.bgs_dict[bg_name]['bg'].first_image, spot['size'])
                scaled_img.set_alpha(spot['alpha'])
                rect = scaled_img.get_rect(center=spot['pos'])
                self.screen.blit(scaled_img, rect)

        self.arrow_left_button.draw(self.screen)
        self.arrow_right_button.draw(self.screen)

        if self.selected_index_menu == 1:
            self.back_button.image = self.back_button.img_off
            self.play_button.image = self.play_button.img_on

        else:
            self.back_button.image = self.back_button.img_on
            self.play_button.image = self.play_button.img_off

        self.back_button.draw(self.screen)
        self.play_button.draw(self.screen)

        pygame.display.update()
        return 'bg_select'
