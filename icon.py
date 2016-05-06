import pygame
import math
from pygame.locals import *


class Icon(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        """ Creates a ball

        Arguments:
            x (int) : x coordinate of screen
            y (int) : y coordinate of screen
            vx (int) : velocity in x-direction of ball
            vy (int) : velocity in y-direction of ball
        """
        # Don't forget to call the super constructor
        super().__init__()

        self.image = image
        # Required for collision detection
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))