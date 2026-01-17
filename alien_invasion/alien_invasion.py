import sys
from time import sleep 
import pygame
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard # !!! НОВЫЙ ИМПОРТ

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion: Survival")

        # --- НАСТРОЙКИ ИГРЫ ---
        self.game_active = True
        self.ships_left = 5       
        self.level = 1            
        self.score = 0 # !!! СЧЕТ
        
        # Настройки сложности
        self.base_ship_speed = 2    # Быстрый корабль
        self.base_alien_speed = 0.1   # Начальная скорость врагов
        self.speedup_scale = 1.1      # Ускорение игры
        self.score_scale = 1.5        # Очки растут с уровнем

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        # Создаем табло счета
        self.sb = Scoreboard(self)

        self.ship.ship_speed = self.base_ship_speed
        self._create_fleet()

    def run_game(self):
        """Основной цикл игры."""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        # !!! УВЕЛИЧИЛ МАГАЗИН ДО 10 ПУЛЬ (было 5)
        if len(self.bullets) < 10:
            new_bullet = Bullet(self)
            # !!! ПУЛИ ТЕПЕРЬ БЫСТРЫЕ (чтобы легче попадать)
            new_bullet.speed = 4.0 
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Проверка попаданий
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions:
            # За каждого сбитого пришельца даем 50 очков
            for aliens in collisions.values():
                self.score += 50 * len(aliens)
            self.sb.prep_score() # Обновляем картинку счета

        if not self.aliens:
            # Если флот уничтожен
            self.bullets.empty()
            self._increase_speed() 
            self.level += 1        
            self.sb.prep_level() # Обновляем картинку уровня
            self._create_fleet()

    def _increase_speed(self):
        self.ship.ship_speed *= self.speedup_scale
        self.base_alien_speed *= self.speedup_scale

    def _update_aliens(self):
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        if self.ships_left > 1:
            self.ships_left -= 1
            print(f"Вас подбили! Осталось жизней: {self.ships_left}")
            
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            
            self.ship.rect.midbottom = self.screen.get_rect().midbottom
            self.ship.x = float(self.ship.rect.x) 
            self.ship.y = float(self.ship.rect.y) 
            
            sleep(1.0)
        else:
            self.game_active = False
            print("GAME OVER")
            # Можно не выходить сразу, но пока оставим как есть
            sys.exit()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = 1200 - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # !!! ВЕРНУЛ 3 РЯДА (ты можешь поставить 1, если сложно)
        for row_number in range(1):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien.alien_speed = self.base_alien_speed
        
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien.y = float(alien.rect.y)
        self.aliens.add(alien)

    def _update_screen(self):
        # Оставил СИНИЙ фон
        self.screen.fill((0, 0, 0)) 
        
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # !!! РИСУЕМ СЧЕТ И УРОВЕНЬ
        self.sb.show_score()

        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
