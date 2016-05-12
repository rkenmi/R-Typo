import pygame
from pygame import *
import pytmx
from pytmx.util_pygame import load_pygame
from player import Player
from player_beam import Beam
from block import Block
from icon import Icon
from enemy import Enemy
import create_enemies
from enemy_bullet import Bullet
from enemy_script import enemy_script
import sys,random
import launcher

# CONSTANTS
SPEED = 5
RESET_COOLDOWN = 10
RECT_COLOR = (0, 255, 255)
FPS = 60
FPS_CLOCK = pygame.time.Clock()
BLACK = pygame.Color(0, 0, 0)

def draw_scrolling_hitbox(surface, tiled_map, hitbox, scroll_x, debug=0):
    hitbox.empty()   # refresh hitbox sprites (due to scrolling)

    for layer in tiled_map.visible_layers:
        if isinstance(layer, pytmx.TiledObjectGroup):
            # iterate over all the objects in the layer
            for obj in layer:
                #print(obj.x, obj.y, obj.width, obj.height)
                if debug:
                    spr = Block(
                            pygame.draw.rect(surface, (0, 0, 255),
                                (obj.x + scroll_x, obj.y, obj.width, obj.height)),
                                )
                else:
                    spr = Block(
                        (obj.x + scroll_x, obj.y, obj.width, obj.height)
                    )

                hitbox.add(spr) # add pytmx map platforms


def update_projectiles(surface, projectiles, hitbox, debug=0):
    for projectile in projectiles:
        if projectile.charging:
            projectile.draw(surface)
        elif not projectile.charging and \
                len(pygame.sprite.spritecollide(projectile, hitbox, False, collision_projectile)) == 0 \
                and not projectile.out_of_screen and not projectile.dead:
            if isinstance(projectile, Bullet):
                hitbox.add(projectile)
            projectile.draw(surface)
            projectile.move()
            if debug:
                pygame.draw.rect(surface, (0, 0, 255),
                     (projectile.rect.x, projectile.rect.y, projectile.image.get_width(), projectile.image.get_height() ))
        else:
            if not projectile.dead and isinstance(projectile, Beam):
                projectile.impact(surface)
            else:
                projectiles.remove(projectile)


def collision_projectile(projectile, target):
    if pygame.sprite.collide_rect(projectile, target):
        # if the player projectile hits the enemy...
        if isinstance(projectile, Beam) and isinstance(target, Enemy):
            target.take_damage(projectile.damage)
            projectile.draw_impact = False
            if projectile.damage < 13:  # weaker beams will not pierce through enemy kills (includes basic beam)
                projectile.dead = True
            if target.dead:
                return False

        # enemy projectiles shouldn't kill the enemy itself if they are touching
        elif isinstance(projectile, Bullet) and isinstance(target, Enemy):
            return False

        # player projectiles and enemy projectiles should pass through each other
        elif isinstance(projectile, Beam) and isinstance(target, Bullet):
            return False

        # same goes for enemy projectiles and other enemy projectiles!
        elif isinstance(projectile, Bullet) and isinstance(target, Bullet):
            return False

        projectile.collide_distance = target.rect.x - projectile.rect.x
        return True
    else:
        return False


def player_handler(surface, player, hitboxes):
    if len(pygame.sprite.spritecollide(player, hitboxes, False, pygame.sprite.collide_mask)) > 0:
        if not player.invincible:
            player.death()
        else:
            player.rect.x = player.last_pos[0] - 1  # offset to compensate for automatic right-scrolling screen
            player.rect.y = player.last_pos[1]


def enemy_handler(surface, player, enemies, hitbox):
    """ Handles enemy movements on surface, giving them rectangle blocks, drawing them, deleting them, etc.

    Parameters:
        surface (Surface) : the screen
        player (pygame.sprite) : the player sprite
        enemies (pygame.sprite.Group) : group of enemy sprites
        hitbox (pygame.sprite.Group) : group of hitbox sprites
    """
    for enemy in enemies:
        enemy.move(-1, 0)
        if enemy.dead_counter == 0:
            hitbox.add(enemy)

        if player.rect.x - enemy.rect.x > surface.get_width():  # if player has passed enemy far enough, kill enemy
            enemy.death(sound=False)  # start dead_counter on enemy

        if enemy.dead_counter < enemy.dead_counter_max:
            enemy.draw(surface)
        else:
            enemies.remove(enemy)


def player_keys_move(surface, player, keys):
    vx, vy = 0, 0
    player.last_pos = (player.rect.x, player.rect.y)

    if keys[pygame.K_w]:
        vy -= SPEED
    elif keys[pygame.K_s]:
        vy += SPEED

    if keys[pygame.K_a]:
        vx -= SPEED
    elif keys[pygame.K_d]:
        vx += SPEED

    player.move(surface, vx, vy)


def player_keys_shoot(surface, player, keys, projectiles, cooldown_counter):
    if keys[pygame.K_SPACE] and not player.charged_beam:
        if cooldown_counter == 0 and not player.dead:
            projectiles.add(
                player.shoot(player.rect.x+player.image.get_width(), player.rect.y+player.image.get_height()/2)
            )
            cooldown_counter += 1  # Initiate cooldown sequence
    elif keys[pygame.K_e]:
        if not player.charged_beam and not player.dead:
            projectiles.add(
                player.shoot(player.rect.x+player.image.get_width()-5, player.rect.y+player.image.get_height()/2, True)
            )
    else:
        if player.charged_beam:
            player.charged_beam.charging = False  # reset charge if no keys are pressed
        player.charged_beam = None  # delete charged beam

    if cooldown_counter == RESET_COOLDOWN:
        cooldown_counter = 0
    elif cooldown_counter > 0:
        cooldown_counter += 1
    return cooldown_counter


def start_level(surface):
    # Code to create the initial window
    window_size = (800, 600)
    #surface = pygame.display.set_mode(window_size)
    surface.fill((0, 0, 0))  # wipe the screen
    bg = pygame.image.load("img/stage.png").convert()
    ready_logo = pygame.image.load("img/ready.gif").convert()
    game_over_logo = pygame.image.load("img/game_over.gif").convert()

    # set up the music
    pygame.mixer.music.load('sounds/music/as_wet_as_a_fish.mp3')

    # set mixer channel to 4 for performance and to prevent sound conflicts
    pygame.mixer.set_num_channels(4)

    hitbox = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    player = Player(100, 280)
    player.draw(surface)

    enemies = create_enemies.get_group(surface)

    # game settings
    lives, scroll_x, stop_enemies = 3, 0, False
    first_play = True

    # counters
    cooldown_counter = 0

    # round fail timer (player died)
    rf_counter = 250

    tiled_map = load_pygame('rtype_tile.tmx')
    alpha_surface = Surface((800, 600)) # The custom-surface of the size of the screen.
    alpha_surface.fill((0, 0, 0))
    alpha = 245
    alpha_surface.set_alpha(alpha)  # Fade out

    while True:  # <--- main game loop

        ####### Key Events #######
        if not first_play:  # disable keys until the game screen loads properly when first time playing
            keys = pygame.key.get_pressed()
            player_keys_move(surface, player, keys)
            cooldown_counter = player_keys_shoot(surface, player, keys, projectiles, cooldown_counter)

        ####### Normal Events #######
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

        surface.blit(bg, (scroll_x, 0)) # SCROLL the background in +x direction

        draw_scrolling_hitbox(surface, tiled_map, hitbox, scroll_x)

        ####### Collisions #######
        enemy_handler(surface, player, enemies, hitbox)
        update_projectiles(surface, projectiles, hitbox)
        player.draw(surface)

        player_handler(surface, player, hitbox)

        ####### UI #######
        pygame.draw.rect(surface, BLACK, (0, 560, 800, 40))
        for i in range (0, lives):
            lives_img = pygame.image.load("sprites/life_icon.gif").convert()
            lives_ico = Icon(100 + (i * 30), 565, lives_img)
            lives_ico.draw(surface)

        ####### Start Round #######
        if player.dead or first_play:
            pygame.mixer.music.stop()
            rf_counter += 1
            if 250 > rf_counter > 200:    # fade out
                alpha += 6
                alpha_surface.set_alpha(alpha)

            elif 300 > rf_counter > 250:
                scroll_x = 0  # stop the scrolling screen
                if not first_play:
                    lives -= 1  # don't deduct life on our first game

                if lives == 0:
                    alpha_surface.blit(game_over_logo, (surface.get_width()/2-game_over_logo.get_width()/2,
                                                        surface.get_height()/2-game_over_logo.get_height()/2))
                else:
                    alpha_surface.blit(ready_logo, (surface.get_width()/2-ready_logo.get_width()/2,
                                                    surface.get_height()/2-ready_logo.get_height()/2))

                enemies = create_enemies.get_group(surface)  # spawn/re-spawn new enemies
                rf_counter = 300

            elif 400 > rf_counter > 350 and lives > 0:  # fade in
                alpha_surface.fill((0, 0, 0))
                alpha -= 6
                alpha_surface.set_alpha(alpha)

            elif rf_counter >= 400 and lives > 0:
                pygame.mixer.music.play(-1, 1.2)  # resume music
                projectiles.empty()
                player.respawn()
                rf_counter = 0
                first_play = False
            elif 600 > rf_counter > 500 and lives == 0:  # game over screen
                alpha_surface.fill((0, 0, 0))
            elif rf_counter > 600 and lives == 0:  # back to beginning game menu
                launcher.main()

            surface.blit(alpha_surface, (0, 0))
        else:
            alpha = 0

        scroll_x -= 1  # Scroll the background to the right by decrementing offset scroll_x

        #  AI for enemies (just a bunch of scripted moves depending on screen location)
        enemy_script(scroll_x, pygame.time.get_ticks(), player, enemies, projectiles)

        pygame.display.update()  # Update the display when all events have been processed
        FPS_CLOCK.tick(FPS)
