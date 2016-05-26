import pygame

from src.enemy.unit.enemy import Enemy


class Moth(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=70, animation_counter=0,
                 start_angle=180):
        """ A single moth unit that usually flies in packs

        Arguments:
            x (int): x coordinate of screen
            y (int): y coordinate of screen
            eid (int): an integer id representation of the particular enemy unit
            animation_counter_max (int): the max counter value before the animation is reset
            dead_counter_max (int): the max counter value before the death animation ends
            animation_counter (int): the current counter value that represents which animation (image) to display.
            start_angle (int): the starting angle (in degrees) the Moth will move towards
        """
        # Don't forget to call the super constructor
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max)

        # Load images
        self.images = []
        self.load_images(start_angle)

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Used as a timer for animation sequences
        self.animation_counter = animation_counter

        # Enemy Configuration
        self.hp = 3
        self.can_shoot = False  # Does not shoot!
        self.idle_animation = False

    def load_images(self, start_angle=180):
        """ A simple method that loads all images for future use.

        Parameters:
            start_angle (int): the starting angle (in degrees) the Moth will move towards

        """
        self.images = []
        if start_angle == 180:
            for i in range(0, 4):
                if i == 2:
                    self.images.append([False, pygame.image.load("sprites/enemy_moth_225.gif").convert()])
                self.images.append(
                    [
                        False, pygame.image.load("sprites/enemy_moth_"+str(i*30+180)+".gif").convert()
                    ]
                )
            self.image = self.images[4][1]
        elif start_angle == 90:
            for i in range(0, 4):
                if i == 2:
                    self.images.append([False, pygame.image.load("sprites/enemy_moth_135.gif").convert()])
                self.images.append(
                    [
                        False, pygame.image.load("sprites/enemy_moth_"+str(i*30+90)+".gif").convert()
                    ]
                )
            self.image = self.images[4][1]