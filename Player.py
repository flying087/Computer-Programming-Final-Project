import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lives = 3

        self.invincible = False
        self.alpha_halved = False

        self.hitbox= pygame.mask.Mask((3, 3), fill=True)
        self.hitbox_rect = self.hitbox.get_rect(center=(x,y))
        self.sprite = pygame.image.load("Sprites/spr_ship_placeholder.png").convert_alpha()

        self.show_hitbox = False

    def draw(self, screen):
        #self.hitbox = pygame.Rect(self.x - 2, self.y - 2, 4, 4)
        sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
        self.hitbox_rect.center = (self.x, self.y)
        screen.blit(self.sprite, sprite_rect)
        if self.show_hitbox == True:
            pygame.draw.rect(screen, "Red", self.hitbox_rect)

    def move(self, h_dir, v_dir):
        self.x += h_dir
        self.y += v_dir

    def iframe(self, alarm):
        if self.invincible == True and alarm != 0:
            alarm -= 1
            if (alarm % 14) > 7:
                self.sprite.set_alpha(122)
            else:
                self.sprite.set_alpha(255)
            return alarm
        else:
            alarm = 180
            self.sprite.set_alpha(255)
            self.invincible = False
            return alarm