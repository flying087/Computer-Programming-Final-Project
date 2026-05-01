import pygame
import math
from Bullets import Boss_Bullet

class Boss:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp

        self.base_sprite = pygame.image.load("Sprites/spr_boss_placeholder.png").convert_alpha()
        self.sprite = self.base_sprite
        self.sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
        self.hitbox = pygame.mask.from_surface(self.sprite)

    def draw(self, screen):
        self.sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
        screen.blit(self.sprite, self.sprite_rect)
        


    def atk_spiral(self, ammount, bullet_array, offset=0):
        for i in range(ammount):
            bullet_array.append(Boss_Bullet(self.x, self.y, (i * 360/ammount) + offset))

    def atk_homing(self, x_target, y_target, bullet_array):
        dx = x_target - self.x
        dy = y_target - self.y

        bullet_array.append(Boss_Bullet(self.x, self.y, math.degrees(math.atan2(dy, dx))))

    def atk_wave(self, bullets_in_wave, starting_direction, space, bullet_array):
        for i in range(bullets_in_wave):
            bullet_array.append(Boss_Bullet(self.x, self.y, starting_direction + i * space))
        
    def move(self, x_target, y_target, speed, weight):


        self.x = pygame.math.lerp(self.x, x_target, weight)
        self.y = pygame.math.lerp(self.y, y_target, weight)

        if round(self.x) == x_target and round(self.y) == y_target:
            return True
        else:
            return False

        # if (self.x >= (x_target - speed)) and ((x_target + speed) >= self.x) and (self.y >= (y_target - speed)) and (self.y <= (y_target + speed)):
        #     return True
        # else:
        #     return False

    def rotate(self, degree):
        self.sprite = pygame.transform.rotate(self.base_sprite, degree)