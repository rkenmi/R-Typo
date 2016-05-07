import pygame
from enemy import Enemy


class SitBot(Enemy):
    def __init__(self, x, y, animation_timer=0):
        # Don't forget to call the super constructor
        super().__init__(x, y)

        # Load images
        self.images = []
        for i in range(0, 3):
            self.images.append(
                [
                    False,
                    pygame.image.load("sprites/enemy_sitbot_stand"+str(i+1)+".gif").convert()
                ]
            )
        self.image = self.images[0][1]

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Variables
        self.hp = 15

        # Used as a timer for animation sequences
        self.animation_timer = animation_timer



