import pygame
from pathlib import Path

class Animation:
    def __init__ (self, folder_path, size, speed=100, mask=False):
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
        self.has_mask = False

        if mask:
            self.mask = pygame.mask.from_surface(self.image)
            self.has_mask = True

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.speed:
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.timer = 0

            if self.has_mask:
                self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen, position):
        rect = self.image.get_rect(topleft=(position))
        screen.blit(self.image, position)
