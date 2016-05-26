import pygame
import math
from pygame.locals import *

ANIMATION_STEP = 3


#  Derive your class from the Sprite super class
class EnemyWeapon(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x=0, target_y=0, play_sound=True):
        """ Creates a circular red bullet used by regular mobs/enemies

        Arguments:
            x (int): x coordinate of screen
            y (int): y coordinate of screen
            target_x (int): x coordinate of target on screen
            target_y (int): y coordinate of target on screen
            play_sound (bool): indicates whether or not the weapon should make sounds. (Not implemented currently)
        """
        # Don't forget to call the super constructor
        super().__init__()

        # Load image
        self.image = None
        self.shoot_images = []
        self.load_images()

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))

        self.mask = pygame.mask.from_surface(self.image, 0)

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y + 35

        # Calculate angle/trajectory of projectile
        self.x0, self.y0 = self.rect.x, self.rect.y # store origin coordinates
        x1, y1 = target_x - x, target_y - y
        magnitude = math.sqrt(math.pow(x1, 2) + math.pow(y1, 2))
        self.x1, self.y1 = (x1 / magnitude), (y1 / magnitude)

        self.move_counter = 0

        # By default, beams do not charge but fire rapidly
        self.charging = False

        # By default, display impact animation for beams
        self.draw_impact = False

        # Flag to remove beam
        self.dead = False

        # Out of screen coords for the beam, to be determined when first drawn
        self.oos_x, self.oos_y = -1, -1

        # Variables
        self.animation_counter = 0
        self.impact_counter = 0
        self.damage = 1
        self.out_of_screen = False

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface (pygame.Surface): Screen pygame object
        """
        self.animation_counter += 1

        for i in range(0, len(self.shoot_images)):
            if self.animation_counter > (i+1)*ANIMATION_STEP:
                self.image = self.shoot_images[i]

        if self.animation_counter > ANIMATION_STEP * 5:
            self.animation_counter = 0

        surface.blit(self.image, (self.rect.x, self.rect.y))
        self.move()

    """
    def bounce(self):
        #  Bounces the ball by inverting the angles.

        if self.hit is False:  # sort of helps with collision/stuck issues when balls hit each other
            magnitude = math.sqrt(math.pow(self.vy, 2) + math.pow(self.vx, 2))
            theta = math.atan2(self.vy, self.vx) # get velocity direction
            theta += math.pi/2  # flip the velocity direction
            self.vx = math.cos(theta) * magnitude
            self.vy = math.sin(theta) * magnitude

        self.hit = not self.hit
    """

    def move(self):
        """ Player 1 beam (lvl 1) moves only in the +x direction

        """
        self.rect.x = self.x0 + self.x1 * self.move_counter
        self.rect.y = self.y0 + self.y1 * self.move_counter
        self.move_counter += 2
        if self.rect.x < self.oos_x or self.rect.y < self.oos_y:
            self.out_of_screen = True

    def impact(self, surface):
        """ Responsible for impact effects, i.e. animation and rectangle adjustments.

        Parameters:
            surface (pygame.Surface): the game screen

        """
        self.damage = 0  # prevent damage from triggering multiple times
        impact_step = 2

        if self.out_of_screen:
            self.dead = True
        elif not self.dead:
            self.impact_counter += 1
            for i in range(0, len(self.impact_images)):
                if i*impact_step < self.impact_counter < (i+1)*impact_step:
                    self.image = self.impact_images[i]

            if self.draw_impact:
                surface.blit(self.image, (self.rect.x+15, self.rect.y-10))

            if self.impact_counter > 6:
                self.dead = True

    def load_images(self):
        """ A simple method that loads all images for future use.

        """
        self.shoot_images = []
        for i in range(0, 4):
            self.shoot_images.append(pygame.image.load("sprites/enemy_wpn1_shoot"+str(i+1)+".gif").convert())
        self.image = self.shoot_images[0]
