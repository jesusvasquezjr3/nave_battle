import pygame
import random
from pathlib import Path
from player import Player
from enemy import Enemy
from powerup import PowerUp
from levels import Level
from laser import Laser

BASE_PATH = Path(__file__).resolve().parent

pathBackgroundMusic = str(BASE_PATH) + '/assets/sounds/background_music.mp3'
pathBackground = str(BASE_PATH) + '/assets/images/background.png'
pathFont = str(BASE_PATH) + '/assets/fonts/universe.ttf'
pathExplosionSound = str(BASE_PATH) + '/assets/sounds/explosion.mp3'
pathPowerupSound = str(BASE_PATH) + '/assets/sounds/powerup_collect.mp3'
pathLaserSound = str(BASE_PATH) + '/assets/sounds/laser_shot.mp3'

class Game:
    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("NAVE BATTLE v1.0")  # Cambiar el nombre de la ventana
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.level = Level(1)
        self.player = Player(self.screen_width, self.screen_height)
        self.enemies = pygame.sprite.Group()
        self.minerals = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.last_mineral_spawn = pygame.time.get_ticks()
        self.enemy_spawn_delay = 1000
        self.mineral_spawn_delay = 2000
        self.minerals_collected = 0
        self.game_over = False
        self.level_complete = False
        self.shots_remaining = 100
        self.show_menu = True
        self.load_level()

        # Cargar sonidos y ajustar volumen
        self.explosion_sound = pygame.mixer.Sound(pathExplosionSound)
        self.powerup_sound = pygame.mixer.Sound(pathPowerupSound)
        self.laser_sound = pygame.mixer.Sound(pathLaserSound)

        # Ajustar el volumen de los sonidos (valores entre 0.0 y 1.0)
        self.explosion_sound.set_volume(0.5)  # Volumen al 50%
        self.powerup_sound.set_volume(0.5)   # Volumen al 50%
        self.laser_sound.set_volume(0.3)     # Volumen al 30%

        # Ajustar el volumen de la música de fondo
        pygame.mixer.music.set_volume(0.3)   # Volumen al 30%

    def load_level(self):
        self.minerals_collected = 0
        self.game_over = False
        self.level_complete = False
        self.enemies.empty()
        self.minerals.empty()
        self.lasers.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.player.health = 100
        self.shots_remaining = 100

    def run(self):
        pygame.mixer.music.load(pathBackgroundMusic)
        pygame.mixer.music.play(-1)  # Reproducir música en bucle
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            if self.show_menu:
                self.draw_start_menu()
            else:
                if not self.game_over and not self.level_complete:
                    self.update()
                self.render()
                if self.game_over:
                    self.draw_game_over()
                if self.level_complete:
                    self.draw_level_complete()
            pygame.display.flip()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.show_menu:
                    if event.key == pygame.K_s:  # Iniciar juego
                        self.show_menu = False
                    if event.key == pygame.K_q:  # Salir del juego
                        self.running = False
                elif self.game_over or self.level_complete:
                    if event.key == pygame.K_r:  # Reiniciar juego
                        self.__init__()
                        self.show_menu = False
                    if event.key == pygame.K_q:  # Salir del juego
                        self.running = False
                elif event.key == pygame.K_SPACE:  # Disparar láser
                    if self.shots_remaining > 0:
                        self.shoot_laser()

    def update(self):
        self.all_sprites.update()
        self.check_collisions()
        self.spawn_enemies()
        self.spawn_minerals()
        self.check_level_complete()

    def spawn_enemies(self):
        now = pygame.time.get_ticks()
        if now - self.last_enemy_spawn > self.enemy_spawn_delay:
            enemy = Enemy(self.level.enemy_speed, self.screen_width, self.screen_height)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn = now
            self.enemy_spawn_delay = random.randint(500, 1500)

    def spawn_minerals(self):
        now = pygame.time.get_ticks()
        if now - self.last_mineral_spawn > self.mineral_spawn_delay:
            mineral = PowerUp(self.screen_width, self.screen_height)
            self.minerals.add(mineral)
            self.all_sprites.add(mineral)
            self.last_mineral_spawn = now
            self.mineral_spawn_delay = random.randint(1000, 3000)

    def shoot_laser(self):
        if self.shots_remaining > 0:
            laser = Laser(self.player.rect.centerx, self.player.rect.top)
            self.lasers.add(laser)
            self.all_sprites.add(laser)
            self.shots_remaining -= 1
            self.laser_sound.play()

    def check_collisions(self):
        for laser in self.lasers:
            enemies_hit = pygame.sprite.spritecollide(laser, self.enemies, True)
            if enemies_hit:
                laser.kill()
                self.explosion_sound.play()
                self.score += 10

        if pygame.sprite.spritecollide(self.player, self.enemies, True):
            self.player.take_damage(10)
            self.explosion_sound.play()
            if self.player.health <= 0:
                self.game_over = True

        if pygame.sprite.spritecollide(self.player, self.minerals, True):
            self.minerals_collected += 1
            self.score += 10
            self.powerup_sound.play()

    def check_level_complete(self):
        if self.minerals_collected >= self.level.minerals_required:
            self.level_complete = True

    def render(self):
        self.screen.blit(pygame.image.load(pathBackground), (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_ui()

    def draw_ui(self):
        font = pygame.font.Font(pathFont, 24)
        score_text = font.render(f"Puntuación: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        health_text = font.render(f"Salud: {self.player.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 40))
        level_text = font.render(f"Nivel: {self.level.number}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 70))
        minerals_text = font.render(f"Minerales: {self.minerals_collected}/{self.level.minerals_required}", True, (255, 255, 255))
        self.screen.blit(minerals_text, (10, 100))
        shots_text = font.render(f"Disparos: {self.shots_remaining}", True, (255, 255, 255))
        self.screen.blit(shots_text, (10, 130))

    def draw_start_menu(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(pathFont, 48)
        title_text = font.render("NAVE BATTLE v1.0", True, (255, 255, 255))  # Cambiar el título del menú
        self.screen.blit(title_text, (self.screen_width // 2 - 200, self.screen_height // 2 - 150))

        font = pygame.font.Font(pathFont, 24)
        instructions = [
            "Instrucciones:",
            "1. Usa las flechas para moverte.",
            "2. Presiona ESPACIO para disparar.",
            "3. Recolecta minerales para completar el nivel.",
            "4. Evita a los enemigos (Están mas cerca de lo que parece)",
            "",
            "Presiona S para empezar o Q para salir."
        ]
        for i, line in enumerate(instructions):
            text = font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (self.screen_width // 2 - 250, self.screen_height // 2 - 50 + i * 30))

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))  # Limpiar la pantalla
        font = pygame.font.Font(pathFont, 48)
        text = font.render("Has sido derribado amigo ;)", True, (255, 0, 0))
        self.screen.blit(text, (self.screen_width // 2 - 150, self.screen_height // 2 - 50))
        font = pygame.font.Font(pathFont, 24)
        text = font.render("Presiona R para Reiniciar o Q para Salir", True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width // 2 - 200, self.screen_height // 2 + 20))

    def draw_level_complete(self):
        self.screen.fill((0, 0, 0))  # Limpiar la pantalla
        font = pygame.font.Font(pathFont, 48)
        text = font.render(f"¡Nivel {self.level.number} Completado!", True, (0, 255, 0))
        self.screen.blit(text, (self.screen_width // 2 - 220, self.screen_height // 2 - 50))
        font = pygame.font.Font(pathFont, 24)
        text = font.render(f"Puntuación: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width // 2 - 80, self.screen_height // 2 + 20))
        text = font.render("Presiona R para Continuar o Q para Salir", True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width // 2 - 220, self.screen_height // 2 + 60))

    def level_up(self):
        self.level.number += 1
        self.level = Level(self.level.number)
        self.minerals_collected = 0
        self.load_level()