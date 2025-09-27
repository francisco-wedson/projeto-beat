import pygame
from pathlib import Path

class Animation:
    def __init__ (self, folder_path, size=(0, 0), speed=10, mask=False, loop=True, flip=False):
        self.frames = []
        path = Path(folder_path)
        for file_path in sorted(path.glob("*.png")):
            img = pygame.image.load(file_path).convert_alpha()
            if size != (0, 0):
                img = pygame.transform.scale(img, size)
            if flip:
                img = pygame.transform.flip(img, True, False)
            self.frames.append(img)

        self.index = 0
        self.timer = 0
        self.fps = speed
        self.loop = loop
        self.finished = False

        self.image = self.frames[self.index]
        self.first_image = self.frames[0]
        self.has_mask = False

        if mask:
            self.mask = pygame.mask.from_surface(self.image)
            self.has_mask = True

    def update(self, dt):
        if self.finished:
            return

        self.timer += dt
        if self.timer >= 1000 / self.fps:
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.timer = 0
            if self.index == len(self.frames) - 1:
                if not self.loop:
                    self.finished = True

            if self.has_mask:
                self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen, position, center=False):
        if center:
            rect = self.image.get_rect(center=(position))
        else:
            rect = self.image.get_rect(topleft=(position))
        screen.blit(self.image, rect)

    def reset(self):
        self.index = 0
        self.timer = 0
        self.finished = False
        self.image = self.frames[self.index]
