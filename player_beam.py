import pygame
import math
from pygame.locals import *

#Derive your class from the Sprite super class
class Beam(pygame.sprite.Sprite):
    def __init__(self, x, y, play_sound=True):
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
        self.sound = pygame.mixer.Sound(file="sounds/player_wpn1.ogg")

        if play_sound:
            self.sound.play()

        # Load image
        self.image = pygame.image.load("sprites/player_wpn1.gif").convert()
        self.impact_images = []
        for i in range(0, 2):
            self.impact_images.append(pygame.image.load("sprites/player_wpn1_impact"+str(i+1)+".gif").convert())

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 15

        # By default, beams do not charge but fire rapidly
        self.charging = False

        # Flag to remove beam
        self.dead = False

        # Variables
        self.impact_timer = 0
        self.damage = 1
        self.out_of_screen = False

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface: Screen pygame object
        """
        surface.blit(self.image, (self.rect.x, self.rect.y))

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

    def move(self, surface):
        """ Player 1 beam (lvl 1) moves only in the +x direction

        Arguments:
            surface (pygame.Surface) : the screen to display
        """

        self.rect.x += self.vx
        if self.rect.x > surface.get_width():
            self.out_of_screen = True

    def impact(self, surface):
        self.damage = 0 # prevent damage from triggering multiple times
        impact_step = 2
        if not self.dead:
            self.impact_timer += 1
            for i in range(0, len(self.impact_images)):
                if i*impact_step < self.impact_timer < (i+1)*impact_step:
                    self.image = self.impact_images[i]

            surface.blit(self.image, (self.rect.x+15, self.rect.y-3))

            if self.impact_timer > 6:
                self.dead = True
