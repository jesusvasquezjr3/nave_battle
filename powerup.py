import pygame
import random
from pathlib import Path
from pygame.sprite import Sprite

BASE_PATH = Path(__file__).resolve().parent

pathMineral = str(BASE_PATH) + '/assets/images/mineral.png'

class PowerUp(Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load(pathMineral)
        self.rect = self.image.get_rect()
        self.rect.x = random.uniform(0, self.screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.screen_height:  # Eliminar si sale de la pantalla
            self.kill()