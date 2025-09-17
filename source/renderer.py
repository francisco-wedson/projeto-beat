import pygame

class Molde(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/teclas/molde.png')
        self.image = pygame.transform.scale(img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Nota(pygame.sprite.Sprite):
    def __init__(self, x, tecla, speed=5):
        y = 1080
        super().__init__()

        self.tecla = tecla

        img = pygame.image.load('assets/teclas/seta.png')
        self.image = pygame.transform.scale(img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y -= self.speed

    def off_screen(self, altura):
        return self.rect.top > altura
