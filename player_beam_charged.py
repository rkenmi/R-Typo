import pygame
import math
from player_beam import Beam
from pygame.locals import *


class ChargedBeam(Beam):
    def __init__(self, x, y):
        """ Creates a beam (level 1)

        Arguments:
            x (int) : x coordinate of screen
            y (int) : y coordinate of screen
            vx (int) : velocity in x-direction of ball
            vy (int) : velocity in y-direction of ball
        """
        # Don't forget to call the super constructor
        super().__init__(x, y)

        self.charge_timer = 0

        # Play the sound file
        self.play_sound()

        # Load image
        self.image = pygame.image.load("sprites/player_wpn2_charge1.gif").convert()

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))

        # Required for collision detection
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.vx = 15
        self.radius = self.image.get_width() / 2
        self.out_of_screen = False
        self.charging = False
        self.charge_level = 0
        self.animation_loop = 0

    def play_sound(self):
        if self.charge_timer == 0:
            clip = pygame.mixer.Sound(file="sounds/player_wpn2.ogg")
            clip.play()


    def draw(self, SCREEN):
        """ Draws to screen

        Arguments:
            SCREEN: Screen pygame object
        """
        if self.charging:
            self.charge_timer += 1
            print(self.charge_level)
            if 0 <= self.charge_timer < 4:
                self.image = pygame.image.load("sprites/player_wpn2_charge2.gif").convert()
                if self.charge_level < 1:
                    self.charge_level = 1
            elif 4 < self.charge_timer < 8:
                self.image = pygame.image.load("sprites/player_wpn2_charge3.gif").convert()
                if self.charge_level < 2:
                    self.charge_level = 2
            elif 8 < self.charge_timer < 12:
                self.image = pygame.image.load("sprites/player_wpn2_charge4.gif").convert()
                if self.charge_level < 3:
                    self.charge_level = 3
            elif 12 < self.charge_timer < 16:
                self.image = pygame.image.load("sprites/player_wpn2_charge5.gif").convert()
                if self.charge_level < 4:
                    self.charge_level = 4
            elif 16 < self.charge_timer < 20:
                self.image = pygame.image.load("sprites/player_wpn2_charge6.gif").convert()
                if self.charge_level < 5:
                    self.charge_level = 5
            elif 20 < self.charge_timer < 24:
                self.image = pygame.image.load("sprites/player_wpn2_charge7.gif").convert()
                if self.charge_level < 6:
                    self.charge_level = 6

                self.charge_timer = 0
                self.play_sound()

        else: # key is let go, or beam is about to shoot
            self.charge_timer = 0
            #print(self.charge_level)
            self.animation_loop += 1
            if self.charge_level == 6:
                if self.animation_loop % 3 == 0:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot1b.gif").convert()
                else:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot1a.gif").convert()

        self.image.set_colorkey(pygame.Color(0, 0, 0))
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))


    def bounce(self):
        """ Bounces the ball by inverting the angles.
        """
        if self.hit is False: # sort of helps with collision/stuck issues when balls hit each other
            magnitude = math.sqrt(math.pow(self.vy, 2) + math.pow(self.vx, 2))
            theta = math.atan2(self.vy, self.vx) # get velocity direction
            theta += math.pi/2 # flip the velocity direction
            self.vx = math.cos(theta) * magnitude
            self.vy = math.sin(theta) * magnitude

        self.hit = not self.hit

    def move(self, SCREEN):
        """ Player 1 beam (lvl 1) moves only in the +x direction

        Arguments:
            x (int): x coord to move
            y (int): y coord to move
        """
        #r_collide = self.rect.x + self.image.get_width() + self.vx > SCREEN.get_width()
        #l_collide = self.rect.x + self.vx < 0
        #t_collide = self.rect.y + self.vy < 0
        #b_collide = self.rect.y + self.image.get_height() + self.vy > SCREEN.get_height()

        # Check collision on right and left sides of screen
        #if l_collide or r_collide:
        #    self.vx *= -1

        # Check collision on top and bottom sides of screen
        #if t_collide or b_collide:
        #    self.vy *= -1

        self.rect.x += self.vx
        if self.rect.x > SCREEN.get_width():
            self.out_of_screen = True