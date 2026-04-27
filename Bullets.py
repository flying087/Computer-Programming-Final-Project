import pygame
import math

class Player_Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y


        self.rect = pygame.Rect(x - 1, y - 6, 2, 6)

        self.in_screen = True

    def draw(self, screen):
        self.rect = pygame.Rect(self.x - 1, self.y - 3, 2, 6)
        pygame.draw.rect(screen, "Yellow", self.rect)

    def move(self):
        self.y -= 8
        if self.y < 0:
            self.in_screen = False



class Boss_Bullet:
    def __init__(self, x, y, degree = 0):
        self.x = float(x)
        self.y = float(y)

        self.base_sprite = pygame.image.load("Sprites/spr_boss_bullet.png").convert_alpha()
        self.sprite = self.base_sprite

        self.sprite_rect = self.sprite.get_rect(center=(self.x, self.y))

        rad = math.radians(degree)
        self.vx = math.cos(rad)
        self.vy = math.sin(rad)

        self.sprite = pygame.transform.rotate(self.base_sprite, -degree)
        self.sprite_rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))

        

    def draw(self, screen):
        screen.blit(self.sprite, self.sprite_rect)

    def rotate(self, degree):
        rad = math.radians(degree)
        self.vx = math.cos(rad)
        self.vy = math.sin(rad)

        self.sprite = pygame.transform.rotate(self.base_sprite, -degree)
        self.sprite_rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))

    def move(self, speed):
        self.x += self.vx * speed
        self.y += self.vy * speed

        self.sprite_rect = self.sprite.get_rect(center=(self.x, self.y))

class Boss_Orb:
    def __init__(self, x, y):
        self.x = x
        self.y = y