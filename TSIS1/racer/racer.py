import pygame
import random
import time
import io
from PIL import Image
from rembg import remove

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        
        filename = f"{color_name}.png"
        input_image = Image.open(filename)
        output_image = remove(input_image)
        image_bytes = io.BytesIO()
        output_image.save(image_bytes, format = "PNG")
        image_bytes.seek(0)
        self.image = pygame.image.load(image_bytes).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)
        self.shielded = False
        
    def move(self, speed_mult):
        pressed_keys = pygame.key.get_pressed()
        move_speed = int(5 * speed_mult)
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-move_speed, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(move_speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, 360), -100)

    def move(self, current_speed):
        self.rect.move_ip(0, int(current_speed))
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()
            return True
        return False

class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        drawing, value = self.get_random_drawing_and_value()
        self.image = pygame.image.load(drawing).convert_alpha()
        self.value = value
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, 380), -50)

    def get_random_drawing_and_value(self):
        chance = random.random()
        if chance < 0.3:
            return ["Coin3.png", 3]
        elif chance < 0.5:
            return ["Coin2.png", 2]
        else:
            return ["Coin1.png", 1]

    def move(self, speed):
        self.rect.move_ip(0, int(speed))
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["Nitro", "Shield", "Repair"])
        if self.type == "Nitro": self.image = pygame.image.load("nitro.png")
        elif self.type == "Shield": self.image = pygame.image.load("shield.png")
        elif self.type == "Repair": self.image = pygame.image.load("repair.png")
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, 380), -50)
        self.spawn_time = time.time()

    def move(self, speed):
        self.rect.move_ip(0, int(speed))
        if self.rect.top > SCREEN_HEIGHT or (time.time() - self.spawn_time) > 8.0:
            self.kill()

class RoadEvent(pygame.sprite.Sprite):
    def __init__(self, event_type):
        super().__init__()
        self.type = event_type
                
        if self.type == "Oil":
            self.image = pygame.image.load("oil.png")
        elif self.type == "NitroStrip":
            self.image = pygame.image.load("arrow.png")
            
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), -100)

    def move(self, speed):
        self.rect.move_ip(0, int(speed))
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()