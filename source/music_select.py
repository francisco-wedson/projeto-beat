import pygame
import json
from .button import BackButton

class MusicSelect:
    def __init__(self, screen, background):
        #Preparação
        self.screen = screen
        self.bg = background
        self.musics = ['All The Things She Said', 'Rebel Yell']
        self.options = [self.musics, 'voltar', 'selecionar']
        self.music_info = {}
        self.mouse_pos = (0, 0)

        self.selected_index_menu = 0
        self.selected_index_music = 0

        #Carregar assets
        self.color_green_normal = (90, 100, 90)
        self.color_green_selected = (35, 254, 37)
        self.color_white = (255, 255, 255)
        self.color_red = (255, 10, 50)
        self.color_blue = (0, 150, 255)
        self.color_normal = (200, 200, 200)
        self.color_selected = (255, 255, 0)
        self.font_music = pygame.font.Font('assets/fontes/PressStart2P-Regular.ttf', 28)
        self.font_select = pygame.font.Font('assets/fontes/Determination.ttf', 84)
        self.font_info = pygame.font.Font('assets/fontes/BebasNeue-Regular.ttf', 64)
        self.font_artist = pygame.font.Font('assets/fontes/BebasNeue-Regular.ttf', 52)
        self.font_year = pygame.font.Font('assets/fontes/BebasNeue-Regular.ttf', 32)
        self.select_button_normal = self.font_select.render("SELECIONAR", True, self.color_green_normal)
        self.select_button_selected = self.font_select.render("SELECIONAR", True, self.color_green_selected)
        self.select_button_rect = self.select_button_normal.get_rect(center=(1440, 530))

        #Overlay
        self.overlay_musics = pygame.Surface((700, 800), pygame.SRCALPHA)
        self.overlay_musics.fill((0, 0, 0, 180))
        self.overlay_details = pygame.Surface((920, 290), pygame.SRCALPHA)
        self.overlay_details.fill((0, 0, 0, 180))

        #Music Info
        with open('assets/menu/music_select/music_info.json', 'r', encoding='utf-8') as f:
            self.music_info_bruto = json.load(f)
        self._load_music_info()

        #Back Button
        self.back_button = BackButton(1120, 530, True)

    def _load_music_info(self):
        y_music = 160
        for music, info in self.music_info_bruto.items():
            self.music_info[music] = info.copy()
            self.music_info[music]['music_path'] = f'assets/musicas/game/{music}/{music}.ogg'
            self.music_info[music]['image_path'] = f'assets/menu/music_select/{music}/{music}.jpg'
            self.music_info[music]['text_info'] = self.font_info.render(music, True, self.color_white)
            self.music_info[music]['text_normal'] = self.font_music.render(music, True, self.color_normal)
            self.music_info[music]['text_selected'] = self.font_music.render(music, True, self.color_selected)
            self.music_info[music]['artist'] = self.font_artist.render(self.music_info[music]['artist'], True, self.color_normal)

            ano_formatado = f"Ano: {self.music_info[music]['year']}"
            self.music_info[music]['year'] = self.font_year.render(ano_formatado, True, self.color_blue)

            duracao_formatado = f"Duração: {self.music_info[music]['time']}"
            self.music_info[music]['time'] = self.font_year.render(duracao_formatado, True, self.color_red)

            rect = self.music_info[music]['text_selected'].get_rect()
            rect.topleft = (120, y_music)
            self.music_info[music]['rect'] = rect
            y_music += 60

    def _draw_info_music(self, music):
        info = self.music_info[music]

        img = pygame.image.load(info['image_path']).convert_alpha()
        img = pygame.transform.scale(img, (250, 250))
        self.screen.blit(img, (920, 160))
        self.screen.blit(info['text_info'], (1190, 150))
        self.screen.blit(info['artist'], (1190, 205))
        self.screen.blit(info['year'], (1190, 260))
        self.screen.blit(info['time'], (1190, 295))

    def run(self, events, dt):
        self.mouse_pos = pygame.mouse.get_pos()

        for i, music in enumerate(self.musics):
            if self.music_info[music]['rect'].collidepoint(self.mouse_pos):
                self.selected_index_music = i

        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return 'char_select'
                if event.key == pygame.K_UP and self.selected_index_menu == 0:
                    self.selected_index_music = (self.selected_index_music + 1) % len(self.musics)

                if event.key == pygame.K_DOWN and self.selected_index_menu == 0:
                    self.selected_index_music = (self.selected_index_music - 1) % len(self.musics)

                if event.key == pygame.K_RIGHT:
                    self.selected_index_menu = (self.selected_index_menu + 1) % len(self.options)

                if event.key == pygame.K_LEFT:
                    self.selected_index_menu = (self.selected_index_menu - 1) % len(self.options)

                if event.key == pygame.K_RETURN:
                    if self.selected_index_menu == 1: return 'char_select'
                    else: return 'bg_select', self.music_info[self.musics[self.selected_index_music]]['music_path']

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.check_click(event): return 'char_select'
                if self.select_button_rect.collidepoint(self.mouse_pos):
                    return 'bg_select', self.music_info[self.musics[self.selected_index_music]]['music_path']

            if self.back_button.check_hover(self.mouse_pos): self.selected_index_menu = 1
            if self.select_button_rect.collidepoint(self.mouse_pos): self.selected_index_menu = 2

        self.bg.update(dt)
        self.bg.draw(self.screen, (0, 0))
        self.screen.blit(self.overlay_musics, (100, 140))
        self.screen.blit(self.overlay_details, (900, 140))

        for i, music in enumerate(self.musics):
            info = self.music_info[music]
            if i == self.selected_index_music and self.selected_index_menu == 0:
                self.screen.blit(info['text_selected'], info['rect'])
            else:
                self.screen.blit(info['text_normal'], info['rect'])

            if info['rect'].collidepoint(self.mouse_pos): 
                self.selected_index_music = i
                self.selected_index_menu = 0
 
        self._draw_info_music(self.musics[self.selected_index_music])

        if self.selected_index_menu == 1:
            pygame.draw.rect(self.screen, self.color_white, self.back_button, 3, border_radius=15)
            self.back_button.image = self.back_button.img_acesa
            self.back_button.draw(self.screen)
            self.screen.blit(self.select_button_normal, self.select_button_rect)

        elif self.selected_index_menu == 2:
            self.back_button.image = self.back_button.img_apagada
            self.back_button.draw(self.screen)
            self.screen.blit(self.select_button_selected, self.select_button_rect)

        else:
            self.back_button.image = self.back_button.img_apagada
            self.back_button.draw(self.screen)
            self.screen.blit(self.select_button_normal, self.select_button_rect)

        pygame.display.update()

        return 'music_select'
