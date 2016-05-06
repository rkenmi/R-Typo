import pygame
import math
from pygame.locals import *

#Derive your class from the Sprite super class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """ Creates a ball

        Arguments:
            x (int) : x coordinate of screen
            y (int) : y coordinate of screen
            vx (int) : velocity in x-direction of ball
            vy (int) : velocity in y-direction of ball
        """
        # Don't forget to call the super constructor
        super().__init__();

        self.image = pygame.image.load("sprites/player.gif").convert()

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))

        # Required for collision detection
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


        # Position to respawn at
        self.respawn_pos = (x, y)
        self.last_pos = (0, 0) # for wall collision

        # 'E' key beam, or charged beam
        self.charged_beam = None

        # Variables
        self.life = 10
        self.dead = False
        self.dead_timer = 0
        self.invincible = False
        self.invincible_timer = 0

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface: Screen pygame object
        """
        if not self.dead and not self.invincible:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        elif not self.dead and self.invincible:
            self.invincible_timer += 1

            if self.invincible_timer % 5 == 0:
                surface.blit(self.image, (self.rect.x, self.rect.y))

            if self.invincible_timer > 90:
                self.invincible = False
                self.invincible_timer = 0
        else:
            if self.dead_timer == 0:
                pygame.mixer.Sound('sounds/player_dead.ogg').play()

            self.dead_timer += 1

            if 10 < self.dead_timer < 25:
                self.image = pygame.image.load("sprites/mob_dead1.gif").convert()
            elif 25 < self.dead_timer < 40:
                self.image = pygame.image.load("sprites/mob_dead2.gif").convert()
            elif 40 < self.dead_timer < 55:
                self.image = pygame.image.load("sprites/mob_dead3.gif").convert()
            elif 55 < self.dead_timer < 70:
                self.image = pygame.image.load("sprites/mob_dead4.gif").convert()
            elif 70 < self.dead_timer < 85:
                self.image = pygame.image.load("sprites/mob_dead5.gif").convert()
            elif 85 < self.dead_timer < 100:
                self.image = pygame.image.load("sprites/mob_dead6.gif").convert()

            if self.dead_timer < 100:
                surface.blit(self.image, (self.rect.x, self.rect.y))



    def death(self):
        self.dead = True
        if self.charged_beam:
            self.charged_beam.charging = False
            self.charged_beam.charge_sound.stop()
            self.charged_beam = None

    def respawn(self):
        self.rect.x = self.respawn_pos[0]
        self.rect.y = self.respawn_pos[1]
        self.dead = False
        self.dead_timer = 0
        self.invincible = True

        # Revert original sprite
        self.image = pygame.image.load("sprites/player.gif").convert()
        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))


    def move(self, surface, x, y):
        """ Moves the beam by altering the x and y coordinates.

        Arguments:
            x (int): x coord to move
            y (int): y coord to move
        """

        if self.dead is False:
            #self.last_pos = (self.rect.x, self.rect.y)

            r_collide = self.rect.x + self.image.get_width() > surface.get_width()
            l_collide = self.rect.x < 0
            t_collide = self.rect.y < 0
            b_collide = self.rect.y + self.image.get_height() > surface.get_height() - 40

            if not ((r_collide and x > 0) or (l_collide and x < 0)):
                self.rect.x += x
                if self.charged_beam:
                    self.charged_beam.rect.x += x

            if not ((t_collide and y < 0) or (b_collide and y > 0)):
                self.rect.y += y
                if self.charged_beam:
                    self.charged_beam.rect.y += y


    def corner_check(self, surface):
        """ Checks if the ball is perfectly aligned in a corner. If so, then a sound will be played.

        Arguments:
            surface: Screen pygame object
        """
        corner_flag = False
        if self.rect.x == 0 and self.rect.y == 0:
            corner_flag = not corner_flag
        elif self.rect.x == 0 and self.rect.y == surface.get_height() - self.image.get_height():
            corner_flag = not corner_flag
        elif self.rect.x == surface.get_width() - self.image.get_width() and self.rect.y == 0:
            corner_flag = not corner_flag
        elif self.rect.x == surface.get_width() - self.image.get_width() and self.rect.y == surface.get_height() - self.image.get_height():
            corner_flag = not corner_flag

        if corner_flag is True:
            #pygame.mixer.Sound('OOT_PressStart.wav').play()
            corner_flag = not corner_flag