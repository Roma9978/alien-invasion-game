import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления снарядами, выпущенными кораблем."""

    def __init__(self, ai_game):
        """Создает объект снаряда в текущей позиции корабля."""
        super().__init__()
        self.screen = ai_game.screen

        # Создание снаряда в позиции (0,0) и назначение правильной позиции.
        self.rect = pygame.Rect(0, 0, 10, 20) # Ширина 3, высота 15
        self.rect.midtop = ai_game.ship.rect.midtop

        # Позиция снаряда хранится в вещественном формате.
        self.y = float(self.rect.y)

        # Цвет и скорость снаряда.
        self.color = (255, 255, 255) # Белый цвет для контраста с черным фоном
        self.speed = 5

    def update(self):
        """Перемещает снаряд вверх по экрану."""
        # Обновление позиции снаряда в вещественном формате.
        self.y -= self.speed
        # Обновление позиции прямоугольника.
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод снаряда на экран."""
        pygame.draw.rect(self.screen, self.color, self.rect)
