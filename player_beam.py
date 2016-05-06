import pygame
import math
from pygame.locals import *

#Derive your class from the Sprite super class
class Beam(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """ Creates a beam (level 1)

        Arguments:
            x (int) : x coordinate of screen
            y (int) : y coordinate of screen
            vx (int) : velocity in x-direction of ball
            vy (int) : velocity in y-direction of ball
        """
        # Don't forget to call the super constructor
        super().__init__();

        # Play the sound file
        s = pygame.mixer.Sound(file="sounds/player_wpn1.ogg")
        s.play()

        # Load image
        self.image = pygame.image.load("sprites/player_wpn1.gif").convert()

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))

        # Required for collision detection
        self.rect = self.image.get_rect()

        # By default, beams do not charge but fire rapidly
        self.charging = False

        self.rect.x = x
        self.rect.y = y
        self.vx = 15
        self.radius = self.image.get_width() / 2
        self.out_of_screen = False

    def draw(self, SCREEN):
        """ Draws to screen

        Arguments:
            SCREEN: Screen pygame object
        """
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