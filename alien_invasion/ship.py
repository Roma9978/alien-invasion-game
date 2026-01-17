import pygame

class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        try:
            self.image = pygame.image.load('images/ship.jpg')
            # ИЗМЕНЕНИЕ 1: Размер теперь 100x100 (был 50x50)
            self.image = pygame.transform.scale(self.image, (100, 100))
        except FileNotFoundError:
            self.image = pygame.Surface((100, 100))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
        # ИЗМЕНЕНИЕ 2: Скорость меньше (было 1.5, стало 0.8)
        self.ship_speed = 0.8

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)
