"""
R-Type Project
CS332L, Spring 2016

Rick Miyamoto
"""
from pygame import *
import pygame, sys
import game
from player import Player

FPS = 60


def main():
    pygame.init()

    fps_clock = pygame.time.Clock()
    # Code to create the initial window

    # set up the music
    pygame.mixer.music.load('sounds/music/solo_sortie.mp3')
    pygame.mixer.music.play(-1, 0.2)  # loop music

    window_size = (800, 600)
    surface = pygame.display.set_mode(window_size)

    # set the title of the window
    pygame.display.set_caption("R-Typo")

    r_type_logo = pygame.image.load("img/main_logo.png").convert()
    r_type_logo.set_colorkey(pygame.Color(0, 0, 0))
    enter_logo = pygame.image.load("img/x-Enter.gif").convert()
    #ship = pygame.image.load("sprites/player.gif").convert()
    #ship.set_colorkey(pygame.Color(0, 0, 0))
    ship = Player(window_size[0]/2 - 30, window_size[1]/2 - 15)
    bg = pygame.image.load("img/space_bg.png")
    text_timer, start_timer  = 0, 0
    scroll_x = 0
    game_start = False
    alpha_surface = Surface((800, 600)) # The custom-surface of the size of the screen.
    alpha_surface.fill((0, 0, 0))
    alpha_surface.set_alpha(0)
    alpha = 0

    while True:
        surface.fill((0, 0, 0))
        surface.blit(bg, (scroll_x, 0))
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, 800, 200))
        pygame.draw.rect(surface, (0, 0, 0), (0, 400, 800, 200))
        surface.blit(r_type_logo, (window_size[0]/2-r_type_logo.get_width()/2,
                                   window_size[1]/4-r_type_logo.get_height()/2 - 50))

        ship.draw(surface)
        text_timer += 1

        if text_timer < 50:
            surface.blit(enter_logo, (window_size[0]/2-enter_logo.get_width()/2,
                                       window_size[1]/2-enter_logo.get_height()/2 + 200))
        elif text_timer > 100:
            text_timer = 0

        scroll_x -= 1
        if scroll_x < -800:
            scroll_x = 0

        if game_start:
            ship.move(surface, 10, 0, bypass_wall=True)  # animation
            start_timer += 1  # start countdown until game mode
            text_timer = 1  # don't blink the text anymore
            if start_timer == 100:
                pygame.mixer.music.fadeout(1000)
            if 200 > start_timer > 100:
                alpha += 5
                alpha_surface.set_alpha(alpha)  # fade out
            elif start_timer >= 200:
                game.start_level(surface)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # enter key
                    game_start = True
                    pygame.mixer.Sound('sounds/start.ogg').play()
                    start_timer = 0

            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

        surface.blit(alpha_surface, (0, 0))
        pygame.display.update()
        fps_clock.tick(FPS)

if __name__ == "__main__":
    main()