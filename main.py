import pygame
from pygame import *
import pytmx
from pytmx.util_pygame import load_pygame
from player import Player
from player_beam import Beam
from block import Block
from icon import Icon
from player_beam_charged import ChargedBeam
from enemy import Enemy
import create_enemies
from enemy_script import enemy_script
import sys,random

# CONSTANTS
SPEED = 5
RESET_COOLDOWN = 10
RECT_COLOR = (0, 255, 255)


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

                hitbox.add(spr) # add pytmx map platforms


def update_beams(surface, beams, hitbox, debug=0):
    for beam in beams:
        if beam.charging:
            beam.draw(surface)
        elif not beam.charging and \
                len(pygame.sprite.spritecollide(beam, hitbox, False, collision_beam_handler)) == 0 \
                and not beam.out_of_screen and not beam.dead:
            beam.draw(surface)
            beam.move()
            if debug:
                pygame.draw.rect(surface, (0, 0, 255),
                     (beam.rect.x, beam.rect.y, beam.image.get_width(), beam.image.get_height() ))
        else:
            if not beam.dead:
                beam.impact(surface)
            else:
                beams.remove(beam)


def collision_beam_handler(beam, obj):
    if pygame.sprite.collide_rect(beam, obj):
        if isinstance(obj, Enemy):
            obj.take_damage(beam.damage)
            beam.draw_impact = False
            if obj.dead:
                return False
        return True
    else:
        return False


def collision_player(surface, player, hitboxes):
    if len(pygame.sprite.spritecollide(player, hitboxes, False, pygame.sprite.collide_rect)) > 0:
        if not player.invincible:
            player.death()
        else:
            player.rect.x = player.last_pos[0] - 1 # offset for screen side-scroll to the right
            player.rect.y = player.last_pos[1]


def enemy_handler(surface, player, enemies, hitbox):
    """ Handles enemy movements on surface, giving them rectangle blocks, drawing them, deleting them, etc.

    Parameters:
        surface (Surface) : the screen
        player (pygame.sprite) : the player sprite
        enemies (pygame.sprite.Group) : group of enemy sprites
        hitbox (pygame.sprite.Group) : group of hitbox sprites
    """
    if not player.dead:
        for enemy in enemies:
            enemy.move(-1, 0)
            if enemy.dead_counter == 0:
                hitbox.add(enemy)

    for enemy in enemies:
        if player.rect.x - enemy.rect.x > surface.get_width(): # if player has passed enemy far enough, kill enemy
            enemy.death(sound=False) # start dead_counter on enemy

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


def player_keys_shoot(surface, player, keys, beams, cooldown_counter):
    if keys[pygame.K_SPACE] and not player.charged_beam:
        if cooldown_counter == 0 and not player.dead:
            beams.add(
                player.shoot(player.rect.x+player.image.get_width(), player.rect.y+player.image.get_height()/2)
            )
            cooldown_counter += 1 # Initiate cooldown sequence
    elif keys[pygame.K_e]:
        if not player.charged_beam and not player.dead:
            beams.add(
                player.shoot(player.rect.x+player.image.get_width()-5, player.rect.y+player.image.get_height()/2, True)
            )
    else:
        if player.charged_beam:
            player.charged_beam.charging = False # reset charge if no keys are pressed
        player.charged_beam = None  # delete charged beam

    if cooldown_counter == RESET_COOLDOWN:
        cooldown_counter = 0
    elif cooldown_counter > 0:
        cooldown_counter += 1
    return cooldown_counter


def main():
    """ Starts bouncing ball animation with kapparinos. Plays a sound if a ball aligns perfectly with corner.
    Balls do bounce fine but they often get stuck to each other and spaz out. Over time, it usually gets itself out.
    Balls may also be generated on top of one another, in which case I would recommend just removing it (minus key)
    and creating a new one (plus key). Numpad keys only.

    Recommended balls: 5-7
    """
    pygame.init()

    FPS = 60
    FPS_CLOCK = pygame.time.Clock()

    # COLOR LIST
    WHITE = pygame.Color(255, 255, 255)
    BLUE = pygame.Color(0, 0, 255)
    BLACK = pygame.Color(0, 0, 0)

    # Code to create the initial window
    window_size = (800, 600)
    surface = pygame.display.set_mode(window_size)
    bg = pygame.image.load("img/stage.png").convert()
    ready_img = pygame.image.load("img/ready.gif").convert()
    #bg = pygame.image.load("img/test.bmp").convert()

    # set the title of the window
    pygame.display.set_caption("R-Typu")

    # set up the music
    pygame.mixer.music.load('sounds/music/solo_sortie.mp3')
    pygame.mixer.music.play(-1, 0.2)  # loop music

    # set mixer channel to 4 for performance and to prevent sound conflicts
    pygame.mixer.set_num_channels(4)

    hitbox = pygame.sprite.Group()
    beams = pygame.sprite.Group()

    player = Player(100, 280)
    player.draw(surface)

    enemies = create_enemies.get_group(surface)

    # game settings
    lives, scroll_x, stop_enemies = 3, 0, False

    # counters
    cooldown_counter = 0
    
    # round fail timer (player died)
    rf_counter = 0

    tiled_map = load_pygame('rtype_tile.tmx')
    alpha_surface = Surface((800, 600)) # The custom-surface of the size of the screen.
    alpha_surface.fill((0, 0, 0))
    alpha_surface.set_alpha(0)
    alpha_surface.blit(ready_img, (400-162,300-27))
    alpha = 0

    while True:  # <--- main game loop
        ####### Key Events #######
        keys = pygame.key.get_pressed()
        player_keys_move(surface, player, keys)
        cooldown_counter = player_keys_shoot(surface, player, keys, beams, cooldown_counter)

        ####### Normal Events #######
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

        surface.blit(bg, (scroll_x, 0)) # SCROLL the background in +x direction

        draw_scrolling_hitbox(surface, tiled_map, hitbox, scroll_x)

        ####### Collisions #######
        enemy_handler(surface, player, enemies, hitbox)
        update_beams(surface, beams, hitbox)
        player.draw(surface)

        collision_player(surface, player, hitbox)

        ####### UI #######
        pygame.draw.rect(surface, BLACK, (0, 560, 800, 40))
        for i in range (0, lives):
            lives_img = pygame.image.load("sprites/life_icon.gif").convert()
            lives_ico = Icon(100 + (i * 30), 565, lives_img)
            lives_ico.draw(surface)

        ####### Round Fail #######
        if player.dead:
            pygame.mixer.music.stop()
            rf_counter += 1

            if 300 > rf_counter > 200:
                alpha += 4
                alpha_surface.set_alpha(alpha) # Fade out

            elif 350 > rf_counter > 300:
                scroll_x = 0
                lives -= 1
                enemies = create_enemies.get_group(surface)
                if lives == 0:
                    sys.exit()
                rf_counter = 350

            elif 450 > rf_counter > 350:
                alpha -= 4
                alpha_surface.set_alpha(alpha)  # Fade in

            elif rf_counter > 450 and lives > 0:
                pygame.mixer.music.play(-1, 0.2) # resume music
                player.respawn()
                rf_counter = 0

            surface.blit(alpha_surface, (0, 0))
        else:
            alpha = 0
            scroll_x -= 1 # Scroll the background to the right by decrementing offset scroll_x

        enemy_script(scroll_x, enemies) # Actions enemies make depending on where the screen is

        pygame.display.update() # Update the display when all events have been processed
        FPS_CLOCK.tick(FPS)

if __name__ == "__main__":
    main()
