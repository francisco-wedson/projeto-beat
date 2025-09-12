import pygame
import os

class Animatedbackground:
    def __init__ (self, folder):
        self.frames = []
        for file in sorted(os.listdir(folder)):
            if file.endswith(".png"):
                img = pygame.image.load(os.path.join(folder, file)).convert()
                self.frames.append(img)

        self.index = 0
        self.timer = 0
        self.speed = 100

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.speed:
            self.index = (self.index + 1) % len(self.frames)
            self.timer = 0

    def draw(self, screen):
        current_frame = self.frames[self.index]

        screen_size = screen.get_size()

        scaled_frame = pygame.transform.scale(current_frame, screen_size)

        screen.blit(scaled_frame, (0,0))
