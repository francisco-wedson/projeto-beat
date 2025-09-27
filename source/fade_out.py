import pygame

class FadeOut:
    def __init__(self, screen, img, img_rect):
        self.screen = screen
        self.img = img
        self.img_rect = img_rect
        self.fade_out_duration = 4000
        self.fade_timer = 0

    def run(self, events, dt):
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'

        self.fade_timer += dt

        if self.fade_timer >= (self.fade_out_duration + 500):
            return 'menu'

        alpha = 255 - int((self.fade_timer / self.fade_out_duration) * 255)
        alpha = max(0, alpha)

        self.screen.fill((0, 0, 0))
        self.img.set_alpha(alpha)
        self.screen.blit(self.img, self.img_rect)
        pygame.display.update()
        return 'fade_out'
