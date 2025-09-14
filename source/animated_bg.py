import pygame
import os

class Animatedbackground:
    def __init__ (self, folder):
        self.frames = []
        try:
            for file in sorted(os.listdir(folder)):
                if file.endswith(".png"):
                    img = pygame.image.load(os.path.join(folder, file)).convert()
                    self.frames.append(img)
        except FileNotFoundError:
            print(f"ERRO: A pasta de animação '{folder}' não foi encontrada.")

        # Verificação para evitar divisão por zero
        if not self.frames:
            print(f"AVISO: Nenhuma imagem .png encontrada em '{folder}'. A animação será desativada.")
            # Se não houver frames, crie um frame preto para evitar crashes
            fallback_frame = pygame.Surface((1, 1))
            fallback_frame.fill((0, 0, 0))
            self.frames.append(fallback_frame)

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
