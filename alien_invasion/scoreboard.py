import pygame.font

class Scoreboard:
    """Класс для вывода игровой информации (очки, уровень)."""

    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчета очков."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Настройки шрифта для вывода счета.
        self.text_color = (255, 255, 255) # Белый текст
        self.font = pygame.font.SysFont(None, 48) # Размер шрифта 48

        # Подготовка исходных изображений.
        self.prep_score()
        self.prep_level()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        score_str = f"Score: {self.ai_game.score}"
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Вывод счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_level(self):
        """Преобразует текущий уровень в графическое изображение."""
        level_str = f"Wave: {self.ai_game.level}"
        self.level_image = self.font.render(level_str, True, self.text_color)

        # Уровень выводится под счетом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        """Выводит счет и уровень на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
