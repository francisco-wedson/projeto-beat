import pygame
from .animation import Animation
from .button import BackButton
from .button import Button

class CharSelect:
    def __init__(self, screen, background, num_players=1):
        #Preparação
        self.screen = screen
        self.bg = background
        self.num_players = num_players

        self.characters = ['pulse', 'echo', 'beat']
        self.available_chars = ['pulse', 'beat']

        self.options = ['voltar', 'selecionar']
        self.selected_index_menu = 1

        self.player_active = 1
        self.choices = {}

        self.selected_index_char = 0
        self.mouse_pos = (0, 0)

        #Carregar assets
        self.font_title = pygame.font.Font('assets/fontes/PressStart2P-Regular.ttf', 48)
        self.font_title_small = pygame.font.Font('assets/fontes/PressStart2P-Regular.ttf', 28)

        self.arrow_select_p1 = pygame.image.load('assets/menu/char_select/selection_arrow_p1.png')
        self.arrow_select_p2 = pygame.image.load('assets/menu/char_select/selection_arrow_p2.png')
        self.arrow_unable_select = pygame.image.load('assets/menu/char_select/selection_arrow_not.png')
        self.arrow_side = pygame.image.load('assets/menu/char_select/side_arrow.png')

        self.arrow_select_p1 = pygame.transform.scale(self.arrow_select_p1, (75, 51))
        self.arrow_select_p2 = pygame.transform.scale(self.arrow_select_p2, (75, 51))
        self.arrow_unable_select = pygame.transform.scale(self.arrow_unable_select, (75, 51))
        self.arrow_side = pygame.transform.scale(self.arrow_side, (60, 34))

        #Dicionário assets
        self.char_assets = {
                        'pulse': Animation('assets/characters_animation/Pulse/Idle Blink', (520, 420), 50, True),
                        'echo': Animation('assets/characters_animation/Echo/Locked', (520, 420), 50, True),
                        'beat': Animation('assets/characters_animation/Beat/Idle Blink', (520, 420), 50, True)
                        }

        #Rotação
        self.img_arrow_side_left = pygame.transform.rotate(self.arrow_side, -90)
        self.img_arrow_side_right = pygame.transform.flip(self.img_arrow_side_left, True, False)

        #Calcula posições e Rects
        self.overlay = pygame.Surface((1352, 540), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        #Spots
        base_size = (520, 420)
        scale_factor_side = 0.8
        side_width = int(base_size[0] * scale_factor_side)
        side_height = int(base_size[1] * scale_factor_side)
        side_size = (side_width, side_height)

        self.spots = {
                'left': {'size': side_size, 'pos': (344 + base_size[0]/2, 240 + base_size[1]), 'alpha': 150},
                'center': {'size': base_size, 'pos': (700 + base_size[0]/2, 240 + base_size[1]), 'alpha': 255},
                'right': {'size': side_size, 'pos': (1056 + base_size[0]/2, 240 + base_size[1]), 'alpha': 150}
        }

        #Superfícies de texto
        self.color_normal = (150, 150, 150)
        self.color_selected = (255, 255, 255)
        self.green_color_normal = (90, 100, 90)
        self.green_color_selected = (144, 238, 144)
        self.color_red = (255, 0, 0)
        self.color_p1_border = (50, 150, 255)

        self.text_selec_normal = self.font_title.render("Selecionar", True, self.green_color_normal)
        self.text_selec_selected = self.font_title.render("Selecionar", True, self.green_color_selected)
        self.text_selec_rect = self.text_selec_normal.get_rect(center=(960, 652))
        self.highlight_rect = self.text_selec_rect.inflate(20, 20)
        self.text_blocked = self.font_title_small.render("Personagem Bloqueado", True, self.color_red)
        self.text_blocked_rect = self.text_blocked.get_rect(center=(960, 206))
        self.text_chosen = self.font_title_small.render("Personagem Escolhido", True, self.color_red)
        self.text_chosen_rect = self.text_chosen.get_rect(center=(960, 206))

        #Botões
        self.back_button = BackButton(304, 200)
        self.arrow_left_button = Button(391, 447, self.img_arrow_side_left)
        self.arrow_right_button = Button(1484, 447, self.img_arrow_side_right)

    def _change_selection(self, direction):
        new_idx = (self.selected_index_char + direction + len(self.characters)) % len(self.characters)
        self.selected_index_char = new_idx

    def _handle_selection(self):
        if self.selected_char_name not in self.available_chars:
            return 'char_select'

        if self.num_players == 2 and self.player_active == 2 and self.selected_char_name == self.choices.get(1):
            return 'char_select'

        self.choices[self.player_active] = self.selected_char_name

        if self.num_players == 2 and self.player_active == 1:
            self.player_active = 2
            self._change_selection(1)
            return 'char_select'
        else:
            return 'music_select', self.choices

    def run(self, events, dt):
        self.mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return 'player_select'

                if event.key == pygame.K_RIGHT:
                    self._change_selection(1)

                if event.key == pygame.K_LEFT:
                    self._change_selection(-1)

                if event.key == pygame.K_UP:
                    self.selected_index_menu = 0

                if event.key == pygame.K_DOWN:
                    self.selected_index_menu = 1

                if event.key == pygame.K_RETURN:
                    if self.selected_index_menu == 1:
                        return self._handle_selection()
                    else: return 'player_select'

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.check_click(event): return 'player_select'
                if self.text_selec_rect.collidepoint(self.mouse_pos):
                    return self._handle_selection()
                if self.arrow_right_button.check_click(event):
                    self._change_selection(1)
                if self.arrow_left_button.check_click(event):
                    self._change_selection(-1)

        if self.text_selec_rect.collidepoint(self.mouse_pos): self.selected_index_menu = 1
        if self.back_button.check_hover(self.mouse_pos): self.selected_index_menu = 0

        self.selected_char_name = self.characters[self.selected_index_char]

        self.bg.update(dt)
        self.bg.draw(self.screen, (0, 0))
        self.screen.blit(self.overlay, (284, 180))

        self.char_assets['pulse'].update(dt)
        self.char_assets['beat'].update(dt)
        self.char_assets['echo'].update(dt)

        center_idx = self.selected_index_char
        left_idx = (self.selected_index_char - 1) % len(self.characters)
        right_idx = (self.selected_index_char + 1) % len(self.characters)

        characters_display = [
            (left_idx, self.spots['left']),
            (right_idx, self.spots['right']),
            (center_idx, self.spots['center'])
        ]

        drawn_char_rects = {}

        for char_index, spot in characters_display:
            char_name = self.characters[char_index]
            current_anim = self.char_assets[char_name]

            scaled_img = pygame.transform.scale(current_anim.image, spot['size'])
            scaled_img.set_alpha(spot['alpha'])

            char_rect = scaled_img.get_rect(centerx=spot['pos'][0], bottom=spot['pos'][1])
            drawn_char_rects[char_name] = char_rect, scaled_img

            self.screen.blit(scaled_img, char_rect)

        if self.selected_char_name in self.available_chars and not self.selected_char_name == self.choices.get(1):
            if self.player_active == 1:
                arrow_to_draw = self.arrow_select_p1
            else:
                arrow_to_draw = self.arrow_select_p2
        else:
            arrow_to_draw = self.arrow_unable_select

        self.screen.blit(arrow_to_draw, (945, 196))

        if self.selected_index_menu == 1:
            pygame.draw.rect(self.screen, self.green_color_selected, self.highlight_rect, 3, border_radius=15)
            self.screen.blit(self.text_selec_selected, self.text_selec_rect)
            self.back_button.image = self.back_button.img_apagada
            self.back_button.draw(self.screen)

        else:
            self.screen.blit(self.text_selec_normal, self.text_selec_rect)
            pygame.draw.rect(self.screen, self.color_selected, self.back_button, 3, border_radius=15)
            self.back_button.image = self.back_button.img_acesa
            self.back_button.draw(self.screen)

        self.arrow_left_button.draw(self.screen)
        self.arrow_right_button.draw(self.screen)

        if self.num_players == 2 and self.player_active == 2:
            p1_choice_name = self.choices[1]
            p1_scaled_img = drawn_char_rects[p1_choice_name][1]
            p1_rect = drawn_char_rects[p1_choice_name][0]

            p1_mask = pygame.mask.from_surface(p1_scaled_img)
            outline_surf = pygame.Surface(p1_rect.size, pygame.SRCALPHA)
            outline_points = p1_mask.outline()
            pygame.draw.polygon(outline_surf, (50, 150, 255), outline_points, 5)
            self.screen.blit(outline_surf, p1_rect.topleft)

        pygame.display.update()
        return 'char_select'
