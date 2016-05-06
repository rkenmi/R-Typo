import pygame
from pygame import *
import pytmx
from pytmx.util_pygame import load_pygame
from player import Player
from player_beam import Beam
from block import Block
from icon import Icon
from player_beam_charged import ChargedBeam
import sys

# CONSTANTS
SPEED = 5
RESET_COOLDOWN = 10
RECT_COLOR = (0, 255, 255)

def update_respawn(surface, player, platforms):
    respawn_x, respawn_y = (player.rect.x, player.rect.y)
    safety_spr = Block(pygame.draw.rect(surface, RECT_COLOR,
            (respawn_x, respawn_y, player.image.get_width(), player.image.get_height()), 3))

    while respawn_y < surface.get_height():
        safety_spr.rect.y = respawn_y
        print('y : ', respawn_y, '\t', len(pygame.sprite.spritecollide(safety_spr, platforms, False, pygame.sprite.collide_rect)))
        if len(pygame.sprite.spritecollide(safety_spr, platforms, False, pygame.sprite.collide_rect)) == 0:
            player.respawn_pos = (respawn_x, respawn_y)
            break
        respawn_y += 10


def draw_scrolling_platforms(surface, tiled_map, platforms, scroll_x, debug=0):
    platforms.empty()   # refresh platform sprites (due to scrolling)

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

                platforms.add(spr)


def update_beams(surface, beams, platforms):
    for beam in beams:
        if beam.charging:
            beam.draw(surface)
        elif not beam.charging and not beam.out_of_screen \
                and len(pygame.sprite.spritecollide(beam, platforms, False, pygame.sprite.collide_rect)) == 0:
            beam.draw(surface)
            beam.move(surface)
        else:
            beams.remove(beam)
    return beams


def collision_detection(surface, player, platforms):
    if len(pygame.sprite.spritecollide(player, platforms, False, pygame.sprite.collide_rect)) > 0:
        if not player.invincible:
            player.death()
        else:
            player.rect.x = player.last_pos[0] - 1 # offset for screen side-scroll to the right
            player.rect.y = player.last_pos[1]


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
    #bg = pygame.image.load("img/test.bmp").convert()

    # set the title of the window
    pygame.display.set_caption("R-Typu")

    # set up the music
    pygame.mixer.music.load('sounds/music/solo_sortie.mp3')
    #pygame.mixer.music.play(-1, 0.2) # loop music

    # set mixer channel to 4 for performance and to prevent sound conflicts
    pygame.mixer.set_num_channels(4)

    platforms = pygame.sprite.Group()
    beams = pygame.sprite.Group()

    player = Player(100, 280)
    player.draw(surface)


    # variables
    lives = 3
    scroll_x = 0
    cooldown_counter, death_counter = 0, 0
    charge_beam = False
    tiled_map = load_pygame('rtype_tile.tmx')
    alpha_surface = Surface((800, 600)) # The custom-surface of the size of the screen.
    alpha_surface.fill((0, 0, 0))
    alpha_surface.set_alpha(0)

    alpha = 0

    while True:  # <--- main game loop
        #update_respawn(surface, player, platforms)  # If player needs to respawn, find best location to respawn


        ####### Key Events #######
        keys = pygame.key.get_pressed()
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

        if keys[pygame.K_SPACE] and not player.charged_beam:
            if cooldown_counter == 0 and not player.dead:
                b = Beam(player.rect.x + player.image.get_width(), player.rect.y + player.image.get_height() / 2)
                beams.add(b)
                cooldown_counter += 1 # Initiate cooldown sequence
        elif keys[pygame.K_e]:
            if not player.charged_beam and not player.dead:
                b = ChargedBeam(player.rect.x + player.image.get_width(), player.rect.y - 20 + player.image.get_height() / 2)
                beams.add(b)
                player.charged_beam = b
                player.charged_beam.charging = True
        else:
            if player.charged_beam:
                player.charged_beam.charging = False # reset charge if no keys are pressed
            player.charged_beam = None  # delete charged beam


        if cooldown_counter == RESET_COOLDOWN:
            cooldown_counter = 0
        elif cooldown_counter > 0:
            cooldown_counter += 1


        ####### Normal Events #######
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

        surface.blit(bg, (scroll_x, 0))
        draw_scrolling_platforms(surface, tiled_map, platforms, scroll_x)

        beams = update_beams(surface, beams, platforms)
        player.draw(surface)

        if player.dead:
            pygame.mixer.music.stop()
            death_counter += 1
            if 300 > death_counter > 200:
                alpha += 4
                alpha_surface.set_alpha(alpha)
            elif 350 > death_counter > 300:
                scroll_x = 0
                lives -= 1
                if lives == 0:
                    sys.exit()
                death_counter = 351
            elif 450 > death_counter > 350:
                alpha -= 4
                alpha_surface.set_alpha(alpha)
            elif death_counter > 450:
                if lives > 0:
                    #pygame.mixer.music.play(-1, 0.2) # resume music
                    player.respawn()
                    death_counter = 0


            surface.blit(alpha_surface, (0, 0))
        else:
            alpha = 0

        collision_detection(surface, player, platforms)

        if not player.dead:
            scroll_x -= 1   # Scroll the background to the right by decrementing offset scroll_x

        pygame.draw.rect(surface, BLACK, (0, 560, 800, 40))

        for i in range (0, lives):
            lives_img = pygame.image.load("sprites/life_icon.gif").convert()
            lives_ico = Icon(100 + (i * 30), 565, lives_img)
            lives_ico.draw(surface)

        pygame.display.update()  # Update the display when all events have been processed
        FPS_CLOCK.tick(FPS)

if __name__ == "__main__":
    main()
