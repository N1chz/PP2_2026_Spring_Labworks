import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()

# Настройки экрана
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# --- ИСПРАВЛЕНИЕ ТУТ: Загружаем и масштабируем фон под размер окна ---
bg_image = pygame.image.load("AnimatedStreet.png")
background = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Глобальные переменные
SCORE = 0
COINS_COLLECTED = 0
ENEMY_SPEED = 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        # Появление только на асфальте (примерные координаты полос)
        self.rect.center = (random.choice([60, 200, 340]), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            # Переспавн на случайной полосе
            self.rect.center = (random.choice([60, 200, 340]), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 3])
        # Визуал монеты
        self.image = pygame.Surface((25, 25))
        if self.weight == 3:
            self.image.fill((255, 215, 0)) # Золотая
        else:
            self.image.fill((192, 192, 192)) # Серебряная
            
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, 4)
        if self.rect.bottom > 600:
            self.reset()

    def reset(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.weight = random.choice([1, 3])
        if self.weight == 3:
            self.image.fill((255, 215, 0))
        else:
            self.image.fill((192, 192, 192))

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона
    DISPLAYSURF.blit(background, (0, 0))
    
    # Текст счета
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_txt = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    spd_txt = font_small.render(f"Speed: {ENEMY_SPEED}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coin_txt, (10, 30))
    DISPLAYSURF.blit(spd_txt, (10, 50))

    # Движение и отрисовка всех спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.5)
        DISPLAYSURF.fill((255, 0, 0))
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Сбор монет
    if pygame.sprite.spritecollide(P1, coins, False):
        for coin in coins:
            SCORE += coin.weight
            COINS_COLLECTED += 1
            # Ускорение врага каждые 5 монет
            if COINS_COLLECTED % 5 == 0:
                ENEMY_SPEED += 1
            coin.reset()

    pygame.display.update()
    FramePerSec.tick(FPS)