# imports
import pygame
import math
import random
from Player import Player
from Bullets import Player_Bullet, Boss_Bullet, Boss_Orb
from Boss import Boss


# constants

# Screen Dimensions

WIDTH = 640
HEIGHT = 480

# frame updates per second
FPS = 60 # use with a clock object

# RGB colors of items on screen
BACKGROUND_COLOR = (0, 0, 0)

PLAYER_SPEED = 4
PLAYER_DAMAGE = 2

# How long the boss attacks for
BOSS_TIMER_SECONDS = 200

pygame.init() # Initiates all pygame modules

# font for everything
font = pygame.font.Font("Font/PixeloidSans-mLxMm.ttf", 8)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final Project")

clock = pygame.time.Clock()

player = Player(320, 240)
boss = Boss(320, 100, 800)


boss.rotate(180)

player_bullets = []

player_bullet_cooldown = 0

room = 0

# The boss timer in FPS
boss_attacks_timer = BOSS_TIMER_SECONDS * FPS
# When this timer expires, the boss attacks randomly

boss_bullets = []
#boss.atk_spiral(100, boss_bullets_test)

# Pre-deicded boss attacks. Format is (boss.attack, (arguments), how many seconds in it should trigger)
boss_attacks_timed =[
    (boss.move, (100, 50, .08), .5),
    (boss.atk_spiral, (10, boss_bullets, 0, 5), 1.5),
    (boss.move, (WIDTH - 100, 50, .08), 2.5),
    (boss.atk_spiral, (10, boss_bullets, 0, 5), 3.5),
    (boss.move, (320, 80, .08), 5),
    (boss.atk_spiral, (50, boss_bullets, 0, 3), 6),
    (boss.move, (120, 380, .08), 7),
    (boss.atk_wave, (40, 200, 5, boss_bullets, 3), 8.5),
    (boss.move, (WIDTH - 120, 380, .08), 9),
    (boss.atk_wave, (40, 280, -5, boss_bullets, 3), 10.5),
    (boss.move, (320, 200), 11),

    (boss.atk_spiral, (60, boss_bullets, 0, .5), 15),
    (boss.atk_spiral, (60, boss_bullets, 45, .5), 15.5),
    (boss.atk_spiral, (60, boss_bullets, 0, .5), 16),
    (boss.atk_spiral, (60, boss_bullets, 45, .5), 16.5),
    (boss.atk_spiral, (60, boss_bullets, 0, .5), 17),
    (boss.atk_spiral, (60, boss_bullets, 45, .5), 17.5),
    (boss.atk_spiral, (60, boss_bullets, 0, .5), 18),

    (boss.move, (320, 50), 19),

    (boss.atk_line, (5, -10, boss_bullets, 5, 90, 4, 20), 20),
    (boss.atk_line, (635, -10, boss_bullets, 5, 90, 4, -20), 20),

    (boss.atk_line, (125, -10, boss_bullets, 5, 90, 4, 20), 21),
    (boss.atk_line, (515, -10, boss_bullets, 5, 90, 4, -20), 21),

    (boss.move, (100, 50), 21.5),

    (boss.atk_homing, (player.x, player.y, boss_bullets, 4), 21.6),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 4), 21.9),

    (boss.atk_line, (245, -10, boss_bullets, 5, 90, 4, 20), 22),
    (boss.atk_line, (395, -10, boss_bullets, 5, 90, 4, -20), 22),

    (boss.move, (440, 50), 23.5),

    (boss.atk_homing, (player.x, player.y, boss_bullets, 4), 24),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 4), 24.5),

    (boss.move, (80, 210), 25.5),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 4), 26),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 4), 26.2),

    (boss.move, (500, 140), 26.8),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 4), 27.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 4), 27.5),

    (boss.atk_wave, (20, 90, 5, boss_bullets, 6), 28),

    (boss.move, (320, 50), 28.5),
    (boss.atk_line, (10, -5, boss_bullets, 32, 90, 2.5, 20), 29),
    (boss.atk_line, (0, -5, boss_bullets, 33, 90, 2.5, 20), 29.5),
    (boss.atk_line, (10, -5, boss_bullets, 32, 90, 2.5, 20), 30),
    (boss.atk_line, (0, -5, boss_bullets, 33, 90, 2.5, 20), 30.5),
    (boss.atk_line, (10, -5, boss_bullets, 32, 90, 2.5, 20), 31),
    (boss.atk_line, (0, -5, boss_bullets, 33, 90, 2.5, 20), 31.5),
    (boss.atk_line, (10, -5, boss_bullets, 32, 90, 2.5, 20), 32),
    (boss.atk_line, (0, -5, boss_bullets, 33, 90, 2.5, 20), 32.5),
    (boss.atk_line, (10, -5, boss_bullets, 32, 90, 2.5, 20), 33),
    (boss.atk_line, (0, -5, boss_bullets, 33, 90, 2.5, 20), 33.5),
    (boss.atk_spiral, (50, boss_bullets, 10, 1), 33.7),
    
    (boss.atk_line, (-5, 10, boss_bullets, 24, 0, 2, 0, 20), 34.5),
    (boss.atk_line, (645, 0, boss_bullets, 25, 180, 2, 0, 20), 35.5),
    (boss.atk_line, (-5, 10, boss_bullets, 24, 0, 2, 0, 20), 36.5),
    (boss.atk_line, (645, 0, boss_bullets, 25, 180, 2, 0, 20), 37.5),
    (boss.atk_line, (-5, 10, boss_bullets, 24, 0, 2, 0, 20), 38.5),
    (boss.atk_line, (645, 0, boss_bullets, 25, 180, 2, 0, 20), 39.5),
    (boss.atk_line, (-5, 10, boss_bullets, 24, 0, 2, 0, 20), 40.5),
    (boss.atk_line, (645, 0, boss_bullets, 25, 180, 2, 0, 20), 41.5),
    (boss.atk_line, (-5, 10, boss_bullets, 24, 0, 2, 0, 20), 42.5),
    (boss.atk_line, (645, 0, boss_bullets, 25, 180, 2, 0, 20), 43.5),

    (boss.atk_spiral_orb, (10, boss_bullets), 45),
    (boss.atk_spiral_orb, (10, boss_bullets, 10), 45.2),
    (boss.atk_spiral_orb, (10, boss_bullets, 20), 45.4),
    (boss.atk_spiral_orb, (10, boss_bullets, 30), 45.6),
    (boss.atk_spiral_orb, (10, boss_bullets, 40), 45.8),
    (boss.atk_spiral_orb, (10, boss_bullets, 50), 46),
    (boss.atk_spiral_orb, (10, boss_bullets, 60), 46.2),
    (boss.atk_spiral_orb, (10, boss_bullets, 70), 46.4),
    (boss.atk_spiral_orb, (10, boss_bullets, 80), 46.6),
    (boss.atk_spiral_orb, (10, boss_bullets, 90), 46.8),

    (boss.move, (600, 110), 47),
    (boss.atk_spiral_orb, (20, boss_bullets, 0, 1), 48),
    (boss.atk_spiral_orb, (20, boss_bullets, 350, 1), 48.2),
    (boss.atk_spiral_orb, (20, boss_bullets, 340, 1), 48.4),
    (boss.atk_spiral_orb, (20, boss_bullets, 330, 1), 48.6),
    (boss.atk_spiral_orb, (20, boss_bullets, 320, 1), 48.8),
    (boss.atk_spiral_orb, (20, boss_bullets, 310, 1), 49),
    (boss.atk_spiral_orb, (20, boss_bullets, 300, 1), 49.2),
    (boss.atk_spiral_orb, (20, boss_bullets, 290, 1), 49.4),
    (boss.atk_spiral_orb, (20, boss_bullets, 280, 1), 49.6),
    (boss.atk_spiral_orb, (20, boss_bullets, 270, 1), 49.8),

    (boss.move, (140, 400), 50),
    (boss.atk_spiral_orb, (20, boss_bullets, 0, 1), 51),
    (boss.atk_spiral_orb, (20, boss_bullets, 10, 1), 51.2),
    (boss.atk_spiral_orb, (20, boss_bullets, 20, 1), 51.4),
    (boss.atk_spiral_orb, (20, boss_bullets, 30, 1), 51.6),
    (boss.atk_spiral_orb, (20, boss_bullets, 40, 1), 51.8),
    (boss.atk_spiral_orb, (20, boss_bullets, 50, 1), 52),
    (boss.atk_spiral_orb, (20, boss_bullets, 60, 1), 52.2),
    (boss.atk_spiral_orb, (20, boss_bullets, 70, 1), 52.4),
    (boss.atk_spiral_orb, (20, boss_bullets, 80, 1), 52.6),
    (boss.atk_spiral_orb, (20, boss_bullets, 90, 1), 52.8),

    (boss.move, (600, 310), 53),
    (boss.atk_spiral_orb, (20, boss_bullets, 0, 1), 54.2),
    (boss.atk_spiral_orb, (20, boss_bullets, 350, 1), 54.4),
    (boss.atk_spiral_orb, (20, boss_bullets, 340, 1), 54.6),
    (boss.atk_spiral_orb, (20, boss_bullets, 330, 1), 54.8),
    (boss.atk_spiral_orb, (20, boss_bullets, 320, 1), 55),
    (boss.atk_spiral_orb, (20, boss_bullets, 310, 1), 55.2),
    (boss.atk_spiral_orb, (20, boss_bullets, 300, 1), 55.4),
    (boss.atk_spiral_orb, (20, boss_bullets, 290, 1), 55.6),
    (boss.atk_spiral_orb, (20, boss_bullets, 280, 1), 55.8),
    (boss.atk_spiral_orb, (20, boss_bullets, 270, 1), 56),
    (boss.atk_spiral_orb, (20, boss_bullets, 260, 1), 56.2),
    (boss.atk_spiral_orb, (20, boss_bullets, 250, 1), 56.4),
    (boss.atk_spiral_orb, (20, boss_bullets, 240, 1), 56.6),
    (boss.atk_spiral_orb, (20, boss_bullets, 230, 1), 56.8),
    (boss.atk_spiral_orb, (20, boss_bullets, 220, 1), 57),
    (boss.atk_spiral_orb, (20, boss_bullets, 210, 1), 57.2),
    (boss.atk_spiral_orb, (20, boss_bullets, 200, 1), 57.4),
    (boss.atk_spiral_orb, (20, boss_bullets, 190, 1), 57.6),
    (boss.atk_spiral_orb, (20, boss_bullets, 180, 1), 57.8),
    (boss.atk_spiral_orb, (20, boss_bullets, 170, 1), 58),


    (boss.move, (440, 310), 59),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 59.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 59.6),
    (boss.move, (380, 260), 60),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 60.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 60.6),
    (boss.move, (200, 110), 61),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 61.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 61.6),
    (boss.move, (80, 440), 62),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 62.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 62.6),
    (boss.move, (170, 330), 63),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 63.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 63.6),
    (boss.move, (170, 200), 64),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 64.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 64.6),
    (boss.move, (280, 250), 65),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 65.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 65.6),
    (boss.move, (390, 100), 66),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 66.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 66.6),
    (boss.move, (500, 220), 67),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 67.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 67.6),
    (boss.move, (370, 310), 68),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 68.3),
    (boss.atk_homing, (player.x, player.y, boss_bullets, 10), 68.6),

    (boss.move, (320, 20), 71),
    
    (boss.atk_spiral_orb, (40, boss_bullets, 0, 4), 73.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 20, 4), 73.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 40, 4), 73.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 60, 4), 73.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 80, 4), 74),
    (boss.atk_spiral_orb, (40, boss_bullets, 100, 4), 74.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 80, 4), 74.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 60, 4), 74.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 40, 4), 74.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 20, 4), 75),
    (boss.atk_spiral_orb, (40, boss_bullets, 0, 4), 75.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 340, 4), 75.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 320, 4), 75.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 300, 4), 75.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 280, 4), 76),
    (boss.atk_spiral_orb, (40, boss_bullets, 260, 4), 76.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 280, 4), 76.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 300, 4), 76.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 320, 4), 76.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 340, 4), 77),
    (boss.atk_spiral_orb, (40, boss_bullets, 0, 4), 77.2),

    (boss.atk_spiral, (50, boss_bullets), 78),
    (boss.atk_spiral, (50, boss_bullets, 45), 78.3),
    (boss.atk_spiral, (50, boss_bullets), 78.6),

    (boss.atk_spiral_orb, (40, boss_bullets, 0, 4), 79.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 20, 4), 79.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 40, 4), 79.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 60, 4), 79.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 80, 4), 80),
    (boss.atk_spiral_orb, (40, boss_bullets, 100, 4), 80.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 80, 4), 80.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 60, 4), 80.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 40, 4), 80.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 20, 4), 81),
    (boss.atk_spiral_orb, (40, boss_bullets, 0, 4), 81.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 340, 4), 81.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 320, 4), 81.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 300, 4), 81.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 280, 4), 82),
    (boss.atk_spiral_orb, (40, boss_bullets, 260, 4), 82.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 280, 4), 82.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 300, 4), 82.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 320, 4), 82.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 340, 4), 83),
    (boss.atk_spiral_orb, (40, boss_bullets, 0, 4), 83.2),

    (boss.atk_spiral, (50, boss_bullets), 84),
    (boss.atk_spiral, (50, boss_bullets, 45), 84.3),
    (boss.atk_spiral, (50, boss_bullets), 84.6),

    (boss.atk_spiral_orb, (40, boss_bullets, 0, 4), 85.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 20, 4), 85.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 40, 4), 85.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 60, 4), 85.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 80, 4), 86),
    (boss.atk_spiral_orb, (40, boss_bullets, 100, 4), 86.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 80, 4), 86.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 60, 4), 86.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 40, 4), 86.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 20, 4), 87),
    (boss.atk_spiral_orb, (40, boss_bullets, 0, 4), 87.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 340, 4), 87.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 320, 4), 87.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 300, 4), 87.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 280, 4), 88),
    (boss.atk_spiral_orb, (40, boss_bullets, 260, 4), 88.2),
    (boss.atk_spiral_orb, (40, boss_bullets, 280, 4), 88.4),
    (boss.atk_spiral_orb, (40, boss_bullets, 300, 4), 88.6),
    (boss.atk_spiral_orb, (40, boss_bullets, 320, 4), 88.8),
    (boss.atk_spiral_orb, (40, boss_bullets, 340, 4), 89),
    (boss.atk_spiral_orb, (40, boss_bullets, 0, 4), 89.2),

    (boss.atk_spiral, (50, boss_bullets), 90),
    (boss.atk_spiral, (50, boss_bullets, 45), 90.3),
    (boss.atk_spiral, (50, boss_bullets), 90.6),

    (boss.atk_line, (0, -5, boss_bullets, 32, 90, 5, 5), 92),
    (boss.atk_line, (640, -5, boss_bullets, 32, 90, 5, -5), 92),

    (boss.atk_line, (320, 485, boss_bullets, 32, 270, 5, -5), 92),
    (boss.atk_line, (320, 485, boss_bullets, 32, 270, 5, 5), 92),

    (boss.atk_line, (-5, 0, boss_bullets, 24, 0, 5, 0, 5), 93),
    (boss.atk_line, (-5, 480, boss_bullets, 24, 0, 5, 0, -5), 93),

    (boss.atk_line, (645, 240, boss_bullets, 24, 180, 5, 0, 5), 93),
    (boss.atk_line, (645, 240, boss_bullets, 24, 180, 5, 0, -5), 93),
]

boss_hp_text = font.render("Boss HP", False, "White")

button_prompt_text = font.render("Press Enter to begin", False, "White")
button_prompt_text_rect = button_prompt_text.get_rect()
button_prompt_text_rect.center = (320, 240)

congrats_text = font.render("Congrats! You beat the boss!", False, "White")
congrats_text_rect = congrats_text.get_rect()
congrats_text_rect.center = (320, 240)

gameover_text = font.render("Game Over", False, "White")
gameover_text_rect = gameover_text.get_rect()
gameover_text_rect.center = (320, 220)

quit_text = font.render("Press Enter to quit", False, "White")
quit_text_rect = quit_text.get_rect()
quit_text_rect.center = (320, 280)

player_iframe_alarm = 3 * FPS


current_boss_movement = None
current_boss_movement_args = None

boss_hp_left = None

boss_attacks_extra_timer = 0
def main():
    running = True
    global player_bullet_cooldown
    global test_bullet_degree
    global boss_attacks_timer
    global boss_attacks_timed
    global boss_bullets
    global current_boss_movement
    global current_boss_movement_args
    global boss_met_target
    global player_iframe_alarm
    global boss_attacks_extra_timer
    global room
    global boss_hp_left
    global congrats_text
    global gameover_text

    while running:
        screen.fill(BACKGROUND_COLOR)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game End")
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if room == 0:
                        room = 1
                    if room == 2 or room == 3:
                        running = False

        if room == 0:
            screen.blit(button_prompt_text, button_prompt_text_rect)

        elif room == 1:
            if player_bullet_cooldown != 0:
                player_bullet_cooldown -= 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z] and player_bullet_cooldown == 0:
                player_bullets.append(Player_Bullet(player.x, player.y, True))
                player_bullets.append(Player_Bullet(player.x - 8, player.y))
                player_bullets.append(Player_Bullet(player.x + 8, player.y))
                player_bullet_cooldown = 10

            player.show_hitbox = False
            if keys[pygame.K_x]:
                PLAYER_SPEED = 1
                player.show_hitbox = True
            else:
                PLAYER_SPEED = 4


            if keys[pygame.K_DOWN] and (player.y + PLAYER_SPEED) <= 480:
                player.y += PLAYER_SPEED
            if keys[pygame.K_UP] and (player.y - PLAYER_SPEED) >= 0:
                player.y -= PLAYER_SPEED
            
            if keys[pygame.K_RIGHT] and (player.x + PLAYER_SPEED) <= 640:
                player.x += PLAYER_SPEED
            if keys[pygame.K_LEFT] and (player.x - PLAYER_SPEED) >= 0:
                player.x -= PLAYER_SPEED


            if current_boss_movement != None and boss_met_target == False:
                boss_met_target = current_boss_movement(*current_boss_movement_args)


            for i in range(len(boss_attacks_timed)):
                if ((BOSS_TIMER_SECONDS - boss_attacks_timed[i][2]) * FPS) == boss_attacks_timer:
                    
                    atk, args, time = boss_attacks_timed[i]
                    if atk.__name__ == "atk_homing":
                        
                        args = ((player.x, player.y, boss_bullets, boss_attacks_timed[i][1][3]))

                    atk(*args)
                    
                    if atk.__name__ == "move":
                        current_boss_movement = atk
                        current_boss_movement_args = args

                        boss_met_target = False

                    if i == len(boss_attacks_timed) - 1:
                        boss_attacks_timer = -1


            if boss_attacks_timer == -1:
                current_boss_movement = boss.move
                boss_met_target = False

                if boss_attacks_extra_timer >= 0 * FPS:
                    current_boss_movement_args = (320, 80, .08)
                if boss_attacks_extra_timer >= 1 * FPS:
                    current_boss_movement_args = (500, 240, .08)
                if boss_attacks_extra_timer >= 2 * FPS:
                    current_boss_movement_args = (320, 400, .08)
                if boss_attacks_extra_timer >= 3 * FPS:
                    current_boss_movement_args = (140, 240, .08)

                if boss_attacks_extra_timer % 40 == 0:
                    boss.atk_spiral_orb(30, boss_bullets, random.randint(0, 90), 1.2)
                elif boss_attacks_extra_timer % 10 == 0:
                    boss.atk_spiral(30, boss_bullets, random.randint(0, 90), 1.4)

                boss_attacks_extra_timer += 1
                if boss_attacks_extra_timer > 4 * FPS:
                    boss_attacks_extra_timer = 0

            # Drawing
                    

            # Draw player bullets at the bottom
            for bullet in range(len(player_bullets) - 1, -1, -1):
                player_bullets[bullet].draw(screen)
                player_bullets[bullet].move(boss)

                offset = (
                    player_bullets[bullet].rect.x - boss.sprite_rect.x,
                    player_bullets[bullet].rect.y - boss.sprite_rect.y
                )

                if player_bullets[bullet].in_screen == False:
                    player_bullets.pop(bullet)
                    continue

                if boss.hitbox.overlap(player_bullets[bullet].hitbox, offset):
                    boss.hp -= 1
                    player_bullets.pop(bullet)
                    continue


            # Draw player above that
            player.draw(screen)

            # Draw boss above that
            boss.draw(screen)

            if player.invincible == True:
                player_iframe_alarm = player.iframe(player_iframe_alarm)

            # Draw boss bullets above that
            for bullet in range(len(boss_bullets) - 1, -1, -1):
                boss_bullets[bullet].draw(screen)
                boss_bullets[bullet].move(2)
                offset = (
                    boss_bullets[bullet].sprite_rect.x - player.hitbox_rect.x,
                    boss_bullets[bullet].sprite_rect.y - player.hitbox_rect.y
                )

                if boss_bullets[bullet].x < -10 or boss_bullets[bullet].x > 650 or boss_bullets[bullet].y < -10 or boss_bullets[bullet].y > 490:
                    boss_bullets.pop(bullet)
                    continue
                    
                if player.hitbox.overlap(boss_bullets[bullet].hitbox, offset) and player.invincible == False:
                    player.lives -= 1
                    player.invincible = True
                    boss_bullets.pop(bullet)


            player_hp_text = font.render(f"Player Lives: {player.lives}", False, "White")



            # GUI elements are drawn last

            # Draws boss health bar
            health_bar = pygame.Rect(5, 5, 10, boss.hp / 4)
            if boss.hp > 0:
                pygame.draw.rect(screen, "Green", health_bar)
            else:
                room = 3

            boss_indicator_sprite = pygame.image.load("Sprites/spr_boss_indicator.png").convert_alpha()
            boss_indicator_rect = boss_indicator_sprite.get_rect(center=(boss.x, 469))
            screen.blit(boss_indicator_sprite, boss_indicator_rect)

            screen.blit(boss_hp_text, (20, 5))
            screen.blit(player_hp_text, (5, 465))
            
            


            if boss_attacks_timer > -1:
                boss_attacks_timer -= 1 # ticks down the timer while it's still active

            if player.lives < 1:
                boss_hp_left = font.render("Boss HP remaining: " + str(boss.hp), False, "White")
                boss_hp_left_rect = boss_hp_left.get_rect()
                boss_hp_left_rect.center = (320, 250)
                room = 2
                
        
        elif room == 2:
            screen.blit(gameover_text, gameover_text_rect)
            screen.blit(boss_hp_left, boss_hp_left_rect)
            screen.blit(quit_text, quit_text_rect)

        elif room == 3:
            screen.blit(congrats_text, congrats_text_rect)
            screen.blit(quit_text, quit_text_rect)

        pygame.display.update()
        clock.tick(FPS)



if __name__ == "__main__":
    main()
    pygame.quit()