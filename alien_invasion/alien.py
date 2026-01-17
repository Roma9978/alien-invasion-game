import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        try:
            self.image = pygame.image.load('images/alien.png')
            self.image = pygame.transform.scale(self.image, (60, 50))
        except FileNotFoundError:
            self.image = pygame.Surface((60, 50))
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Скорость падения пришельца
        self.alien_speed = 0.3

    def update(self):
        """Перемещает пришельца вниз."""
        self.y += self.alien_speed
        self.rect.y = self.y
