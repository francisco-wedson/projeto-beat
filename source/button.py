import pygame

class Button():
    def __init__(self, x, y, img_apagada, img_acesa=None):
        self.img_apagada = img_apagada
        self.img_acesa = img_acesa
        self.image = self.img_apagada
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.rect))

    def toggle_image(self):
        if self.image == self.img_apagada:
            self.image = self.img_acesa
        else:
            self.image = self.img_apagada

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False
