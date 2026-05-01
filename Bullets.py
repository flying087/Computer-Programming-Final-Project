import pygame
import math

class Player_Bullet:
    def __init__(self, x, y, homing=False):
        self.x = x
        self.y = y
        self.homing = homing

        self.base_sprite = pygame.image.load("Sprites/spr_player_bullet.png").convert_alpha()
        self.sprite = self.base_sprite

        self.rect = self.sprite.get_rect(center=(self.x, self.y-3))

        self.in_screen = True
        
        rect_surface = pygame.Surface((self.rect.width, self.rect.height))

        self.hitbox = pygame.mask.from_surface(rect_surface)

    def draw(self, screen):
        #self.rect = pygame.Rect(self.x - 1, self.y - 3, 2, 6)
        #pygame.draw.rect(screen, "Yellow", self.rect)

        screen.blit(self.sprite, self.rect)

    def move(self, target=None):
        if self.homing == False:
            self.sprite = pygame.transform.rotate(self.base_sprite, 90)
            self.y -= 8
            self.rect.center = (self.x, self.y)
        else:
            dx = target.x - self.x
            dy = target.y - self.y
            
            rad = (math.atan2(dy, dx))
            degree = math.degrees(rad)
            
                               
            self.vx = math.cos(rad)
            self.vy = math.sin(rad)

            self.sprite = pygame.transform.rotate(self.base_sprite, -degree)
            self.rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))

            self.x += self.vx * 8
            self.y += self.vy * 8

            self.sprite_rect = self.sprite.get_rect(center=(self.x, self.y))

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

        self.hitbox = pygame.mask.from_surface(self.sprite)
        self.hitbox_drawn = self.hitbox.to_surface(None, None, None, (0, 255, 0), (0, 0, 0, 0))

        

    def draw(self, screen):
        
        #pygame.draw.rect(screen, "Green", self.sprite_rect)
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