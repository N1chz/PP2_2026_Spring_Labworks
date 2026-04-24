import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# FPS setup
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY  = (100, 100, 100)
YELLOW = (255, 255, 0)

# Game variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

# Road scrolling
road_y = 0
road_speed = 5

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, BLACK)

# Load background (road)
try:
    background = pygame.image.load("AnimatedStreet.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    print("Warning: 'AnimatedStreet.png' not found. Creating fallback road.")
    # Create a simple gray road with yellow center line
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(GRAY)
    # Yellow dashed center line
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(background, YELLOW, (SCREEN_WIDTH//2 - 5, y, 10, 20))

# Set up display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("Player.png")
        except FileNotFoundError:
            self.image = pygame.Surface((40, 70))
            self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("Enemy.png")
        except FileNotFoundError:
            self.image = pygame.Surface((40, 70))
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Setup sprites
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Speed increase event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Scroll road
    road_y += road_speed
    if road_y >= SCREEN_HEIGHT:
        road_y = 0

    # Draw road (scrolling effect)
    DISPLAYSURF.blit(background, (0, road_y - SCREEN_HEIGHT))
    DISPLAYSURF.blit(background, (0, road_y))

    # Draw score
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Update and draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Collision detection
    if pygame.sprite.spritecollideany(P1, enemies):
        try:
            crash_sound = pygame.mixer.Sound('crash.wav')
            crash_sound.play()
        except:
            pass  # Ignore if sound file missing

        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (30, 250))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)