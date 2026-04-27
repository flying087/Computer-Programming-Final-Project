import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100

        self.hitbox = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
        self.sprite = pygame.image.load("Sprites/ship_placeholder.png").convert_alpha()

    def draw(self, screen):
        self.hitbox = pygame.Rect(self.x - 2, self.y - 2, 4, 4)
        sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
        screen.blit(self.sprite, sprite_rect)
        pygame.draw.rect(screen, "Green", self.hitbox)

    def move(self, h_dir, v_dir):
        self.x += h_dir
        self.y += v_dir
