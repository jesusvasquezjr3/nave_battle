import pygame
from pathlib import Path
from pygame.sprite import Sprite

BASE_PATH = Path(__file__).resolve().parent

pathPlayerShip = str(BASE_PATH) + '/assets/images/player_ship.png'

class Player(Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load(pathPlayerShip)  # Cargar imagen sin escalar
        self.rect = self.image.get_rect()  # El rect se ajusta al tamaño de la imagen
        self.rect.center = (self.screen_width // 2, self.screen_height - 100)
        self.health = 100
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Limitar movimiento dentro de la pantalla
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def collect_powerup(self):
        self.health += 20
        if self.health > 100:
            self.health = 100