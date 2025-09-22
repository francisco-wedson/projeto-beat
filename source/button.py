import pygame

class Button():
    def __init__(self, x, y, img_apagada, img_acesa=None, center=None):
        self.img_apagada = img_apagada
        self.img_acesa = img_acesa
        self.image = self.img_apagada
        if center:
            self.rect = self.image.get_rect(center=(x, y))
        else:
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

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

class BackButton(Button):
    def __init__(self, x, y, center=None):
        img_off = pygame.image.load("assets/menu/buttons/voltar_off.png").convert_alpha()
        img_on = pygame.image.load("assets/menu/buttons/voltar_on.png").convert_alpha()

        img_off = pygame.transform.scale(img_off, (60, 48))
        img_on = pygame.transform.scale(img_on, (60, 48))
        super().__init__(x, y, img_off, img_on, center)
