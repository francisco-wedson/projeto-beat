import pygame
from .button import BackButton

class PlayerSelect():
    def __init__(self, screen, background):
        #Preparação
        self.screen = screen
        self.bg = background
        self.options = ['voltar', 'solo', 'versus']
        self.selected_index = 1
        self.mouse_pos = (0, 0)

        #Carregar assets
        self.font_title = pygame.font.Font('assets/fontes/PressStart2P-Regular.ttf', 48)
        self.font_x = pygame.font.Font('assets/fontes/Stencilia-A.ttf', 90)

        self.img_solo = pygame.image.load('assets/menu/player_select/Echo_player_select.png').convert_alpha()
        self.img_vs1 = pygame.image.load('assets/menu/player_select/Beat_player_select.png').convert_alpha()
        self.img_vs2 = pygame.image.load('assets/menu/player_select/Pulse_player_select.png').convert_alpha()
        self.img_vs0_no_light = pygame.image.load('assets/menu/player_select/vs_img_no_light.png').convert_alpha()
        self.img_vs0_light = pygame.image.load('assets/menu/player_select/vs_img_light.png').convert_alpha()

        self.img_solo = pygame.transform.scale(self.img_solo, (256, 320))
        self.img_vs1 = pygame.transform.scale(self.img_vs1, (256, 320))
        self.img_vs2 = pygame.transform.scale(self.img_vs2, (256, 320))
        self.img_vs0_no_light = pygame.transform.scale(self.img_vs0_no_light, (100, 100))
        self.img_vs0_light = pygame.transform.scale(self.img_vs0_light, (100, 100))

        #Rotação e flip
        self.img_vs1 = pygame.transform.rotate(self.img_vs1, -25)
        self.img_vs2 = pygame.transform.flip(self.img_vs2, True, False)
        self.img_vs2 = pygame.transform.rotate(self.img_vs2, -30)

        #Calcula posições e Rects
        card_width, card_height = 450, 600
        self.hitbox_solo = pygame.Rect(435, 240, card_width, card_height)
        self.hitbox_vs = pygame.Rect(1035, 240, card_width, card_height)

        self.overlay = pygame.Surface((1170, 720), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        self.img_solo_rect = self.img_solo.get_rect(center=(660, 520))
        self.img_vs1_rect = self.img_vs1.get_rect(center=(1160, 480))
        self.img_vs2_rect = self.img_vs2.get_rect(center=(1340, 680))
        self.img_vs0_rect = self.img_vs0_light.get_rect(center=(1260, 580))

        #Superfícies de texto
        self.color_normal = (150, 150, 150)
        self.color_selected = (255, 255, 255)

        self.text_solo_normal = self.font_title.render("Solo", True, self.color_normal)
        self.text_solo_selected = self.font_title.render("Solo", True, self.color_selected)
        self.text_solo_rect = self.text_solo_normal.get_rect(centerx=self.hitbox_solo.centerx, top=self.hitbox_solo.top + 30)

        self.text_vs_normal = self.font_title.render("Versus", True, self.color_normal)
        self.text_vs_selected = self.font_title.render("Versus", True, self.color_selected)
        self.text_vs_rect = self.text_vs_normal.get_rect(centerx=self.hitbox_vs.centerx, top=self.hitbox_vs.top + 30)

        #Botão de Voltar
        self.back_button = BackButton(400, 195)

        self.clickable_elements = {
            'voltar': self.back_button.rect,
            'solo': self.hitbox_solo,
            'versus': self.hitbox_vs
        }

    def run(self, events, dt):
        self.mouse_pos = pygame.mouse.get_pos()

        for i, option_name in enumerate(self.options):
            if self.clickable_elements[option_name].collidepoint(self.mouse_pos):
                self.selected_index = i

        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return 'menu'
                if event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)

                if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)

                if event.key == pygame.K_RETURN:
                    player_mode = self.options[self.selected_index]
                    if player_mode == "voltar": return 'menu'
                    if player_mode == "solo": return 'char_select', 1
                    if player_mode == "versus": return 'char_select', 2

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.check_click(event): return 'menu'
                if self.hitbox_solo.collidepoint(self.mouse_pos): return 'char_select', 1
                if self.hitbox_vs.collidepoint(self.mouse_pos): return 'char_select', 2

        self.bg.update(dt)
        self.bg.draw(self.screen, (0, 0))
        self.screen.blit(self.overlay, (375, 180))

        self.screen.blit(self.img_solo, self.img_solo_rect)

        if self.selected_index == 0:
            self.back_button.image = self.back_button.img_acesa
            self.back_button.draw(self.screen)
            pygame.draw.rect(self.screen, self.color_selected, self.back_button, 3, border_radius=15)

        else:
            self.back_button.image = self.back_button.img_apagada
            self.back_button.draw(self.screen)

        if self.selected_index == 1:
            pygame.draw.rect(self.screen, self.color_selected, self.hitbox_solo, 3, border_radius=15)
            self.screen.blit(self.text_solo_selected, self.text_solo_rect)
        else:
            self.screen.blit(self.text_solo_normal, self.text_solo_rect)

        self.screen.blit(self.img_vs1, self.img_vs1_rect)
        self.screen.blit(self.img_vs2, self.img_vs2_rect)

        if self.selected_index == 2:
            pygame.draw.rect(self.screen, self.color_selected, self.hitbox_vs, 3, border_radius=15)
            self.screen.blit(self.text_vs_selected, self.text_vs_rect)
            self.screen.blit(self.img_vs0_light, self.img_vs0_rect)

        else:
            self.screen.blit(self.text_vs_normal, self.text_vs_rect)
            self.screen.blit(self.img_vs0_no_light, self.img_vs0_rect)

        pygame.display.update()
        return 'player_select'
