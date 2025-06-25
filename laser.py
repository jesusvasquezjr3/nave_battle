import pygame
from pathlib import Path
from pygame.sprite import Sprite

BASE_PATH = Path(__file__).resolve().parent
pathLaser = str(BASE_PATH) + '/assets/images/laser.png'

class Laser(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(pathLaser)  # Cargar imagen del láser
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -20  # Velocidad del láser (hacia arriba)

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:  # Eliminar el láser si sale de la pantalla
            self.kill()