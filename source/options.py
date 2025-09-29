import pygame
import json
import os
from .button import BackButton

class OptionsMenu:
    def __init__(self, screen, background, config):
        self.screen = screen
        self.bg = background
        self.selected_idx = 0
        self.mouse_pos = (0, 0)
        self.waiting_key = None

        self.font_text = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 28)

        self.overlay_size = (1170, 720)
        self.overlay = pygame.Surface(self.overlay_size, pygame.SRCALPHA)
        self.overlay_rect = self.overlay.get_rect(topleft=(375, 180))
        pygame.draw.rect(self.overlay, (0, 0, 0, 180), self.overlay.get_rect(), border_radius=15)

        self.color_normal = (150, 150, 150)
        self.color_selected = (255, 255, 255)

        self.back_button = BackButton(400, 195)
        self.config = config

        self.option_list = ["back", "volume_menu", "volume_game"]
        for player in ["player1", "player2"]:
            for key_name in ["left", "down", "up", "right"]:
                self.option_list.append(f"{player}_{key_name}")

    def save_config(self, config=None):
        if config is None:
            config = self.config
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)

    def activate_option(self, idx):
        name = self.option_list[idx]
        if name == "back":
            return "menu"
        if name == "volume_menu":
            self.config["volume"]["menu"] = round(self.config["volume"]["menu"] + 0.1, 1)
            if self.config["volume"]["menu"] > 1.0:
                self.config["volume"]["menu"] = 0.0
            self.save_config()
        elif name == "volume_game":
            self.config["volume"]["game"] = round(self.config["volume"]["game"] + 0.1, 1)
            if self.config["volume"]["game"] > 1.0:
                self.config["volume"]["game"] = 0.0
            self.save_config()
        elif "player1" in name or "player2" in name:
            player, key_name = name.split("_")[0], "_".join(name.split("_")[1:])
            self.waiting_key = (player, key_name)
        return None

    def draw_option(self, text, x, y, idx):
        color = self.color_selected if self.selected_idx == idx else self.color_normal
        render = self.font_text.render(text, True, color)
        rect = render.get_rect(topleft=(x, y))
        self.screen.blit(render, rect)
        if color == self.color_selected:
            pygame.draw.rect(self.screen, self.color_selected, rect.inflate(20, 10), 3, border_radius=8)
        return rect

    def draw_keys(self, player, x, y_start):
        title_render = self.font_text.render(player.upper(), True, self.color_normal)
        self.screen.blit(title_render, (x, y_start - 40))
        rects = []
        for key_name, key_value in self.config["keybinds"][player].items():
            rect = self.draw_option(f"{key_name}: {key_value}", x, y_start, self.option_list.index(f"{player}_{key_name}"))
            rects.append(rect)
            y_start += 50
        return rects

    def run(self, events, dt):
        self.mouse_pos = pygame.mouse.get_pos()

        self.bg.update(dt)
        self.bg.draw(self.screen, (0, 0))
        self.screen.blit(self.overlay, self.overlay_rect)
        pygame.draw.rect(self.screen, (234, 0, 255), self.overlay_rect, 3, border_radius=15)

        self.back_button.image = self.back_button.img_on if self.selected_idx == 0 else self.back_button.img_off
        self.back_button.draw(self.screen)

        rects = []
        rects.append(self.draw_option(f"Volume Menu: {self.config['volume']['menu']}", 500, 300, 1))
        rects.append(self.draw_option(f"Volume Jogo: {self.config['volume']['game']}", 500, 350, 2))
        rects.extend(self.draw_keys("player1", 500, 500))
        rects.extend(self.draw_keys("player2", 950, 500))

        if self.back_button.check_hover(self.mouse_pos):
            self.selected_idx = 0
        else:
            for i, rect in enumerate(rects):
                if rect.collidepoint(self.mouse_pos):
                    self.selected_idx = i + 1

        for event in events:
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if self.waiting_key:
                    player, key_to_change = self.waiting_key
                    self.config["keybinds"][player][key_to_change] = pygame.key.name(event.key)
                    self.save_config()
                    self.waiting_key = None
                else:
                    if event.key == pygame.K_UP:
                        self.selected_idx = (self.selected_idx - 1) % len(self.option_list)
                    if event.key == pygame.K_DOWN:
                        self.selected_idx = (self.selected_idx + 1) % len(self.option_list)
                    if event.key == pygame.K_RETURN:
                        result = self.activate_option(self.selected_idx)
                        if result == "menu":
                            return "menu"
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.rect.collidepoint(self.mouse_pos):
                    return "menu"
                for i, rect in enumerate(rects):
                    if rect.collidepoint(self.mouse_pos):
                        self.activate_option(i + 1)

        pygame.display.update()
        return "options"

