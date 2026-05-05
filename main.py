# imports
import pygame
import math
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

# How long the boss 
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


# The boss timer in FPS
boss_attacks_timer = BOSS_TIMER_SECONDS * FPS
# When this timer expires, the boss attacks randomly

boss_bullets = []
#boss.atk_spiral(100, boss_bullets_test)

# Pre-deicded boss attacks. Format is (boss.attack, (arguments), how many seconds in it should trigger)
boss_attacks_timed =[
    (boss.move, (100, 50, 2, .08), .5),
    (boss.atk_spiral, (10, boss_bullets, 0, 5), 1.5),
    (boss.move, (WIDTH - 100, 50, 2, .08), 2.5),
    (boss.atk_spiral, (10, boss_bullets, 0, 5), 3.5),
    (boss.move, (320, 80, 2, .08), 5),
    (boss.atk_spiral, (50, boss_bullets, 0, 3), 6),
    (boss.move, (120, 380, 2, .08), 7),
    (boss.atk_wave, (40, 200, 5, boss_bullets, 3), 8.5),
    (boss.move, (WIDTH - 120, 380, 2, .08), 9),
    (boss.atk_wave, (40, 280, -5, boss_bullets, 3), 10.5),
    (boss.move, (320, 200, 2, .03), 11),

    (boss.atk_spiral, (60, boss_bullets, 0, .5), 13),
    (boss.atk_spiral, (60, boss_bullets, 45, .5), 13.5),
    (boss.atk_spiral, (60, boss_bullets, 0, .5), 14),
    (boss.atk_spiral, (60, boss_bullets, 45, .5), 14.5),
    (boss.atk_spiral, (60, boss_bullets, 0, .5), 15),
    (boss.atk_spiral, (60, boss_bullets, 45, .5), 15.5),
    (boss.atk_spiral, (60, boss_bullets, 0, .5), 16),

    (boss.atk_line, (500, 100, boss_bullets, 5, 90, 2, 10), 17),
]

boss_hp_text = font.render("Boss HP", False, "White")

player_iframe_alarm = 3 * FPS

current_boss_movement = None
current_boss_movement_args = None
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

    while running:
        screen.fill(BACKGROUND_COLOR)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game End")
                running = False

        

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
            PLAYER_SPEED = 2
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
                    args = ((player.x, player.y, boss_bullets))

                atk(*args)
                
                if atk.__name__ == "move":
                    current_boss_movement = atk
                    current_boss_movement_args = args

                    boss_met_target = False



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

        boss_indicator_sprite = pygame.image.load("Sprites/spr_boss_indicator.png").convert_alpha()
        boss_indicator_rect = boss_indicator_sprite.get_rect(center=(boss.x, 469))
        screen.blit(boss_indicator_sprite, boss_indicator_rect)

        screen.blit(boss_hp_text, (20, 5))
        screen.blit(player_hp_text, (5, 465))
        
        


        if boss_attacks_timer > -1:
            boss_attacks_timer -= 1 # ticks down the timer while it's still active

        if player.lives < 1:
            gameover_text = font.render("Game Over", False, "White")
            screen.blit(gameover_text, (320, 240))

        pygame.display.update()
        clock.tick(FPS)



if __name__ == "__main__":
    main()
    pygame.quit()