import math

import pygame

from src.enemy.weapon.enemy_wpn import EnemyWeapon

ANIMATION_STEP = 3


#  Derive your class from the Sprite super class
class EnemyWeaponMissile(EnemyWeapon):
    def __init__(self, x, y, t1, play_sound=True, random_aim=0):
        """ Creates a missile that launches upward and falls down.

        Arguments:
            x (int): x coordinate of screen
            y (int): y coordinate of screen
            t1 (int): the max animation counter. The notation could be seen as time subscript 1 or time_1.
            play_sound (bool): if True, play sound of the weapon. (Not implemented yet)
            random_aim (int): gives the weapon a random offset to the y-distance
        """
        # Don't forget to call the super constructor
        super().__init__(x, y, 0, 0, play_sound)

        self.random_aim = random_aim
        # Load image
        self.shoot_images = []
        self.load_images()

        self.animation_counter = 0
        self.x0, self.y0 = x, y
        self.t1 = t1

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface (pygame.Surface): Screen pygame object
        """
        if self.animation_counter < self.t1:

            if 0 <= self.animation_counter < 25:
                self.image = self.shoot_images[0]
            elif 25 <= self.animation_counter < 35:
                self.image = self.shoot_images[1]
            elif 35 <= self.animation_counter < 43:
                self.image = self.shoot_images[2]
            elif 42 <= self.animation_counter < 50:
                self.image = self.shoot_images[3]
            elif 50 <= self.animation_counter < 51:
                self.image = self.shoot_images[4]
            elif 51 <= self.animation_counter < 59:
                self.image = self.shoot_images[5]
            elif 59 <= self.animation_counter < 67:
                self.image = self.shoot_images[6]
            elif 67 <= self.animation_counter < 77:
                self.image = self.shoot_images[7]
            elif 77 <= self.animation_counter < self.x1:
                self.image = self.shoot_images[8]

            self.move()
            self.animation_counter += 1
            surface.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        """ Missiles move in a upside-down parabola trajectory with some randomness

        """
        t = self.animation_counter

        if 0 <= t < (50 + self.random_aim):
            self.rect.x -= 1
            self.rect.y -= math.sqrt(math.sqrt(math.fabs(50 - t)))
        else:  # negative
            self.rect.x -= 1
            self.rect.y += math.sqrt(math.sqrt(math.fabs(t - 50)))

    def load_images(self):
        """ A simple method that loads all images for future use.

        """
        self.shoot_images = []
        for i in range(0, 7):
            if i == 2:
                self.shoot_images.append(pygame.image.load("sprites/enemy_transformer_wpn_135.gif").convert())
            if i == 5:
                self.shoot_images.append(pygame.image.load("sprites/enemy_transformer_wpn_225.gif").convert())
            self.shoot_images.append(pygame.image.load("sprites/enemy_transformer_wpn_"+str(i*30 + 90)+".gif").convert())
        self.image = self.shoot_images[0]

