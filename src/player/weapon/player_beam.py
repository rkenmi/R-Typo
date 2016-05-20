import pygame
import math
from pygame.locals import *


#  Derive your class from the Sprite super class
class PlayerWeapon(pygame.sprite.Sprite):
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
        self.load_images()

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 15

        # By default, beams do not charge but fire rapidly
        self.charging = False

        # By default, display impact animation for beams
        self.draw_impact = True

        # Flag to remove beam
        self.dead = False

        # Out of screen coords for the beam, to be determined when first drawn
        self.oos_x, self.oos_y = -1, -1

        # Variables
        self.collide_distance = 0  # this value gets filled when the beam hits something (like a wall)
        self.impact_timer = 0
        self.damage = 1
        self.out_of_screen = False

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface: Screen pygame object
        """
        # Only trigger once, when drawn for the first time
        offset = 50  # make it "look" like the beam is actually traveling past the screen
        if self.oos_x == -1 and self.oos_y == -1:
            self.oos_x, self.oos_y = surface.get_width() - self.image.get_width() + offset, \
                                     surface.get_height() - self.image.get_height() + offset

        surface.blit(self.image, (self.rect.x, self.rect.y))

    def bounce(self):
        """ Bounces the ball by inverting the angles.
        """
        if self.hit is False:  # sort of helps with collision/stuck issues when balls hit each other
            magnitude = math.sqrt(math.pow(self.vy, 2) + math.pow(self.vx, 2))
            theta = math.atan2(self.vy, self.vx) # get velocity direction
            theta += math.pi/2  # flip the velocity direction
            self.vx = math.cos(theta) * magnitude
            self.vy = math.sin(theta) * magnitude

        self.hit = not self.hit

    def move(self):
        """ Player 1 beam (lvl 1) moves only in the +x direction

        Arguments:
            surface (pygame.Surface) : the screen to display
        """

        self.rect.x += self.vx
        if self.rect.x > self.oos_x:
            self.out_of_screen = True

    def impact(self, surface):
        self.damage = 0 # prevent damage from triggering multiple times
        impact_step = 2

        if self.out_of_screen:
            self.dead = True
        elif not self.dead:
            self.impact_timer += 1
            for i in range(0, len(self.impact_images)):
                if i*impact_step < self.impact_timer < (i+1)*impact_step:
                    self.image = self.impact_images[i]

            if self.draw_impact:
                surface.blit(self.image, (self.rect.x+15, self.rect.y-10))

            if self.impact_timer > 6:
                self.dead = True

    def load_images(self):
        self.image = pygame.image.load("sprites/player_wpn1.gif").convert()
        self.impact_images.clear()
        for i in range(0, 2):
            self.impact_images.append(pygame.image.load("sprites/player_wpn1_impact"+str(i+1)+".gif").convert())

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))
