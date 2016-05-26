import pygame
import math
from pygame.locals import *


class Block(pygame.sprite.Sprite):
    def __init__(self, rect):
        """ Creates a Block, an invisible sprite that represents a hitbox or a collide-able object.
        Utilizes a mask to improve accuracy of collision.

        Arguments:
            rect (Set): a set of coordinates to create a rectangle with.
        """
        # Don't forget to call the super constructor
        super().__init__()

        # Required for collision detection
        self.rect = pygame.Rect(rect)
        w, h = int(rect[2]), int(rect[3])
        self.mask = pygame.mask.Mask((w, h))
        self.mask.fill()
