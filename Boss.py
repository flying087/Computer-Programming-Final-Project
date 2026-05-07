import pygame
import math
from Bullets import Boss_Bullet, Boss_Orb

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
        


    def atk_spiral(self, ammount, bullet_array, offset=0, bullet_speed = 2):
        for i in range(ammount):
            bullet_array.append(Boss_Bullet(self.x, self.y, (i * 360/ammount) + offset, bullet_speed))

    def atk_spiral_orb(self, ammount, bullet_array, offset=0, orb_speed = 2):
        for i in range(ammount):
            bullet_array.append(Boss_Orb(self.x, self.y, (i * 360/ammount) + offset, orb_speed))

    def atk_homing(self, x_target, y_target, bullet_array, bullet_speed = 2):
        dx = x_target - self.x
        dy = y_target - self.y

        bullet_array.append(Boss_Bullet(self.x, self.y, math.degrees(math.atan2(dy, dx)), bullet_speed))

    def atk_wave(self, bullets_in_wave, starting_direction, space, bullet_array, bullet_speed = 2):
        for i in range(bullets_in_wave):
            bullet_array.append(Boss_Bullet(self.x, self.y, starting_direction + i * space, bullet_speed))
            # Bullets go clockwise normally

    def atk_line(self, bullet_x, bullet_y, bullet_array, bullets_in_row=1, direction=0, bullet_speed=2, bullet_spacing_x=5, bullet_spacing_y=0):
        for i in range(bullets_in_row):
            bullet_array.append(Boss_Bullet(bullet_x, bullet_y, direction, bullet_speed))
            bullet_x += bullet_spacing_x # Positive bullet spacing moves to the right, negative moves to the left
            bullet_y += bullet_spacing_y # Positiev bullet spacing moves up, negative moves down
        
    def move(self, x_target, y_target, weight=.03):


        self.x = pygame.math.lerp(self.x, x_target, weight)
        self.y = pygame.math.lerp(self.y, y_target, weight)

        if round(self.x) == x_target and round(self.y) == y_target:
            return True
        else:
            return False


    def rotate(self, degree):
        self.sprite = pygame.transform.rotate(self.base_sprite, degree)