import pygame

class Button():
    def __init__(self, x, y, img_off, img_on=None, center=None):
        self.img_off = img_off
        self.img_on = img_on
        self.image = self.img_off
        if center:
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.rect))

    def toggle_image(self):
        if self.image == self.img_off:
            self.image = self.img_on
        else:
            self.image = self.img_off

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
