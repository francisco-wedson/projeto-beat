import pygame
from pathlib import Path

class Animation:
    def __init__ (self, folder_path, size, speed=100):
        self.frames = []
        path = Path(folder_path)
        for file_path in sorted(path.glob("*.png")):
            img = pygame.image.load(file_path).convert_alpha()
            scaled_img = pygame.transform.scale(img, size)
            self.frames.append(scaled_img)

        self.index = 0
        self.timer = 0
        self.speed = speed

        self.image = self.frames[self.index]

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.speed:
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.timer = 0

    def draw(self, screen, position):
        rect = self.image.get_rect(topleft=(position))
        screen.blit(self.image, position)
