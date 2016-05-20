import pygame
import pytmx
import sys
from pytmx.util_pygame import load_pygame

import launcher
from src.enemy import enemy_script
from src.enemy.unit.enemy import Enemy
from src.enemy.weapon.enemy_bullet import EnemyWeapon
from src.misc import *
from src.player.unit.player import Player
from src.player.weapon.player_beam import PlayerWeapon

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
                if debug:
                    spr = Block(
                            pygame.draw.rect(surface, (0, 0, 255),
                                (obj.x + scroll_x, obj.y, obj.width, obj.height)),
                                )
                else:
                    spr = Block(
                        (obj.x + scroll_x, obj.y, obj.width, obj.height)
                    )

                hitbox.add(spr)  # add pytmx map platforms


def update_projectiles(surface, projectiles, hitbox, debug=0):
    for projectile in projectiles:
        if projectile.charging:
            projectile.draw(surface)
        elif not projectile.charging and \
                len(pygame.sprite.spritecollide(projectile, hitbox, False, collision_projectile)) == 0 \
                and not projectile.out_of_screen and not projectile.dead:
            if isinstance(projectile, EnemyWeapon):
                hitbox.add(projectile)
            projectile.draw(surface)
            projectile.move()
            if debug:
                pygame.draw.rect(surface, (0, 0, 255),
                     (projectile.rect.x, projectile.rect.y, projectile.image.get_width(), projectile.image.get_height() ))
        else:
            if not projectile.dead and isinstance(projectile, PlayerWeapon):
                projectile.impact(surface)
            else:
                projectiles.remove(projectile)


def collision_projectile(projectile, target):
    if pygame.sprite.collide_rect(projectile, target):
        # if the unit projectile hits the enemy...
        if isinstance(projectile, PlayerWeapon) and isinstance(target, Enemy):
            if target.invincible:
                return False
            else:
                target.take_damage(projectile.damage)

            projectile.draw_impact = False
            if projectile.damage < 13:  # weaker beams will not pierce through enemy kills (includes basic beam)
                projectile.dead = True
            if target.dead:  # allows projectile to pass through after a kill
                return False

        # enemy projectiles shouldn't kill the enemy itself if they are touching
        elif isinstance(projectile, EnemyWeapon) and isinstance(target, Enemy):
            return False

        # unit projectiles and enemy projectiles should pass through each other
        elif isinstance(projectile, PlayerWeapon) and isinstance(target, EnemyWeapon):
            return False

        # same goes for enemy projectiles and other enemy projectiles!
        elif isinstance(projectile, EnemyWeapon) and isinstance(target, EnemyWeapon):
            return False

        projectile.collide_distance = target.rect.x - projectile.rect.x
        return True
    else:
        return False


def player_handler(surface, player, hitboxes, scroll):
    if len(pygame.sprite.spritecollide(player, hitboxes, False, pygame.sprite.collide_mask)) > 0:
        if not player.invincible:
            player.death()
        else:
            if scroll:
                player.rect.x = player.last_pos[0] - 1  # offset to compensate for automatic right-scrolling screen
            else:
                player.rect.x = player.last_pos[0]
            player.rect.y = player.last_pos[1]


def enemy_handler(surface, player, enemies, hitbox, scroll):
    """ Handles enemy movements on surface, giving them rectangle blocks, drawing them, deleting them, etc.

    Parameters:
        surface (pygame.Surface) : the screen
        player (pygame.sprite) : the player unit sprite
        enemies (pygame.sprite.Group) : group of enemy sprites
        hitbox (pygame.sprite.Group) : group of hitbox sprites
        scroll (bool) : True if the screen is scrolling, False if the screen is paused and fixed.
    """
    for enemy in enemies:
        if scroll:
            enemy.move(-1, 0)
        if enemy.dead_counter == 0:
            hitbox.add(enemy)

        if player.rect.x - enemy.rect.x > surface.get_width():  # if unit has passed enemy far enough, kill enemy
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
    pygame.mixer.music.load('sounds/music/solo_sortie.mp3')

    hitbox = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    player = Player(100, 280)
    player.draw(surface)

    # game settings
    lives, scroll, scroll_x, stop_enemies = 3, True, 0, False
    game_start = True  # a flag that is checked before the very first play-through
    game_pause, boss_pause = False, False  # flags that pause the game.
    # game pause is caused by user.
    # boss pause is event triggered.

    player_lock = False  # locks unit keyboard actions only
    boss_timer = 0  # a timer that keeps track of the boss's action sequences (see enemy_script.py)
    boss_pause_timer, win_pause_timer = 0, 0  # timers for pauses caused by game events
    round_clear = False  # a flag for the game to start ending
    play_win_theme = False  # a flag to play the victory theme

    enemies = enemy_script.create_enemies(surface, scroll_x)


    # counters
    cooldown_counter = 0

    # round fail timer (unit died)
    rf_counter = 250

    tiled_map = load_pygame('tilemap/rtype_tile.tmx')
    alpha_surface = pygame.Surface((800, 600)) # The custom-surface of the size of the screen.
    alpha_surface.fill((0, 0, 0))
    alpha = 245
    alpha_surface.set_alpha(alpha)  # Fade out

    while True:  # <--- main game loop
        #  Normal Events
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # enter key
                    game_pause = not game_pause
                    pygame.mixer.Sound('sounds/start.ogg').play()

            if event.type == pygame.QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

        if not game_start and not game_pause:  # the following are not needed when the game first starts
            #  Key Events
            if not player_lock:
                keys = pygame.key.get_pressed()
                player_keys_move(surface, player, keys)
                cooldown_counter = player_keys_shoot(surface, player, keys, projectiles, cooldown_counter)
    
            surface.blit(bg, (scroll_x, 0)) # SCROLL the background in +x direction
    
            draw_scrolling_hitbox(surface, tiled_map, hitbox, scroll_x)
    
            #  Collisions
            enemy_handler(surface, player, enemies, hitbox, scroll)
            update_projectiles(surface, projectiles, hitbox)
            player.draw(surface)
    
            player_handler(surface, player, hitbox, scroll)

            #  UI
            pygame.draw.rect(surface, BLACK, (0, 560, 800, 40))
            for i in range (0, lives):
                lives_ico = Icon(100 + (i * 30), 565)
                lives_ico.draw(surface)

        #  Start Round
        if player.dead or game_start:
            pygame.mixer.music.stop()
            rf_counter += 1
            if 250 > rf_counter > 200:    # fade out
                alpha += 6
                alpha_surface.set_alpha(alpha)

            elif 300 > rf_counter > 250:
                scroll_x = 0  # reset scrolling screen
                scroll = True
                boss_timer = 0
                if not game_start:
                    lives -= 1  # don't deduct life on our first game

                if lives == 0:
                    alpha_surface.blit(game_over_logo, (surface.get_width()/2-game_over_logo.get_width()/2,
                                                        surface.get_height()/2-game_over_logo.get_height()/2))
                else:
                    alpha_surface.blit(ready_logo, (surface.get_width()/2-ready_logo.get_width()/2,
                                                    surface.get_height()/2-ready_logo.get_height()/2))

                enemies = enemy_script.create_enemies(surface, scroll_x)  # spawn/re-spawn new enemies
                projectiles.empty()
                rf_counter = 300

            elif 400 > rf_counter > 350 and lives > 0:  # fade in
                alpha_surface.fill((0, 0, 0))
                alpha -= 6
                alpha_surface.set_alpha(alpha)

            elif rf_counter >= 400 and lives > 0:
                pygame.mixer.music.load('sounds/music/solo_sortie.mp3')
                pygame.mixer.music.play(-1, 0.2)  # resume music
                player.respawn()
                rf_counter = 0
                game_start = False
            elif 600 > rf_counter > 500 and lives == 0:  # game over screen
                alpha_surface.fill((0, 0, 0))
            elif rf_counter > 600 and lives == 0:  # back to beginning game menu
                launcher.main()

            surface.blit(alpha_surface, (0, 0))
        else:
            if not round_clear:
                alpha = 0

        if not game_start and not game_pause and scroll_x > -5800:
            scroll_x -= 1  # Scroll the background to the right by decrementing offset scroll_x
        elif -5850 < scroll_x <= -5800:
            pygame.mixer.music.fadeout(1000)
            scroll_x -= 1
        elif scroll_x <= -5850:
            if scroll:
                pygame.mixer.music.load('sounds/music/boss.mp3')
                pygame.mixer.music.play()
                scroll = False
                boss_pause_timer = 4000 + pygame.time.get_ticks()
                player_lock = True
            if pygame.time.get_ticks() >= boss_pause_timer:
                if player_lock:
                    player_lock = False

                if not game_pause:
                    boss_timer += 1
                    if boss_timer > 300:
                        boss_timer = 1

        #  Enemies follow a script until the stage is cleared (or the game is paused)
        if not round_clear and not game_pause:
            round_clear = enemy_script.load(scroll_x, boss_timer, player, enemies, projectiles)

        if round_clear:
            if not play_win_theme:
                player.be_invincible(animation=False)
                play_win_theme = True
                pygame.mixer.music.load('sounds/music/victory.mp3')
                pygame.mixer.music.play()
                boss_pause_timer = 6000 + pygame.time.get_ticks()
                alpha_surface.blit(game_over_logo, (surface.get_width()/2-game_over_logo.get_width()/2,
                                                    surface.get_height()/2-game_over_logo.get_height()/2))
            if pygame.time.get_ticks() >= boss_pause_timer:
                alpha += 2
                alpha_surface.set_alpha(alpha)
                surface.blit(alpha_surface, (0, 0))
                if alpha > 800:
                    launcher.main()

        pygame.display.update()  # Update the display when all events have been processed
        FPS_CLOCK.tick(FPS)
