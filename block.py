import pygame
import math
from pygame.locals import *

#Derive your class from the Sprite super class
class Block(pygame.sprite.Sprite):
    def __init__(self, rect):
        """ Creates a ball

        Arguments:
            x (int) : x coordinate of screen
            y (int) : y coordinate of screen
            vx (int) : velocity in x-direction of ball
            vy (int) : velocity in y-direction of ball
        """
        # Don't forget to call the super constructor
        super().__init__();

        # Required for collision detection
        self.rect = rect