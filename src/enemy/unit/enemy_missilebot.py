import random

import pygame
from pygame.locals import *

from src.enemy.unit.enemy import Enemy
from src.enemy.weapon.enemy_missile import EnemyWeaponMissile

ANIMATION_STEP = 15  # time between each animation sprite


class MissileBot(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=70, animation_counter=0):
        """ Creates a MissileBot, capable of shooting missiles upward

        Arguments:
            x (int): x coordinate of screen
            y (int): y coordinate of screen
            eid (int): an integer id representation of the particular enemy unit
            animation_counter_max (int): the max counter value before the animation is reset
            dead_counter_max (int): the max counter value before the death animation ends
            animation_counter (int): the current counter value that represents which animation (image) to display.
        """
        # Don't forget to call the super constructor
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max)

        # Enemy Configuration
        self.hp = 6
        self.can_shoot = False
        self.idle_animation = True
        self.launch_animation = False
        self.stand_y = y - 28
        self.idle_y = y
        self.y0 = y

        # Load images
        self.load_images()

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Used as a timer for animation sequences
        self.animation_counter = animation_counter

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface (pygame.Surface): Screen pygame object
        """
        if not self.dead:  # enemy is alive
            animation_step = 10
            stand = False
            self.animation_counter += 1

            if self.hit_animation: # enemy was hit with a beam
                self.hit_timer() # start hit timer

            if self.idle_animation:
                for i in range(0, len(self.images)+1):
                    if i == len(self.images) and self.animation_counter > (i+1)*animation_step:
                        self.image = self.images[0][1]
                    elif self.animation_counter > (i+1)*animation_step and not self.images[i][0]:
                        self.images[i][0] = True
                        self.image = self.images[i][1]

                if self.animation_counter >= self.animation_counter_max:
                    self.animation_counter = 0
                    for i in range(0, len(self.images)):
                        self.images[i][0] = False
            else:
                for i in range(6, len(self.images)):
                    if self.animation_counter > (i+1)*animation_step and not self.images[i][0]:
                        self.images[i][0] = True
                        self.image = self.images[i][1]
                        if i == 6:
                            self.rect.y = self.y0 - 11
                        elif i >= 7:
                            self.rect.y = self.y0 - 35

                if self.animation_counter > 150:
                    self.can_shoot = True

            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect() # update rect to fix moving hitboxes
            self.rect.x, self.rect.y = x, y

            self.image.set_colorkey(pygame.Color(0, 0, 0))
            if not self.hit_animation:
                surface.blit(self.image, (self.rect.x, self.rect.y))
            else:
                surface.blit(self.image, (self.rect.x, self.rect.y), None, BLEND_RGBA_ADD)
        else: # enemy is about to die, start dead timer
            dead_step = 10
            if self.dead_counter == 0 and not self.mute:
                self.death_sound.play()

            self.dead_counter += 2

            # enemy can't move while dead, but the animation must align with the scrolling screen
            self.move(-1, 0, bypass=True)

            for i in range(0, len(self.dead_images)):
                if (i+1)*dead_step < self.dead_counter < (i+2)*dead_step:
                    self.image = self.dead_images[i]

            self.image.set_colorkey(pygame.Color(0, 0, 0))
            if self.dead_counter < self.dead_counter_max:
                surface.blit(self.image, (self.rect.x, self.rect.y))

    def shoot(self, target_x, target_y, charged=False):
        """ The enemy shoots some projectile at the unit. Some enemies can do this, others can't.

        Arguments:
            target_x (int): x coordinate of the aimed location
            target_y (int): y coordinate of the aimed location
            charged (bool): True/False depending on whether it is a charged beam or not

        Returns:
            A newly created EnemyWeapon object
        """
        if self.can_shoot and -800 < self.rect.x - target_x < 800:
            return EnemyWeaponMissile(self.rect.x + 30, self.rect.y - 50, 150, random_aim=random.randint(0, 4)*5)

    def flip_sprite(self):
        """ Flip the sprite from right to left or left to right. Also changes the facing.

        """
        if self.facing == 'left':
            self.facing = 'right'
        else:
            self.facing = 'left'

        self.load_images()

    def siege_mode(self):
        """ A method specific to the MissileBot. Allows attacks to commence once in siege mode, but the transition
        into siege mode takes a few seconds, leaving it vulnerable.

        """
        self.unpause()
        self.idle_animation = False

    def load_images(self):
        """ A simple method that loads all images for future use.

        """
        self.images = []
        if self.facing == 'right':
            for i in range(0, 3):
                self.images.append(
                    [
                        False, pygame.image.load("sprites/enemy_giru"+str(i+1)+"r.gif").convert()
                    ]
                )
            self.images.append([False, pygame.image.load("sprites/enemy_giru2r.gif").convert()])
        else:  # if facing left
            for i in range(0, 6):
                self.images.append(
                    [
                        False, pygame.image.load("sprites/enemy_transformer"+str(i+1)+".gif").convert()
                    ]
                )
            for i in range(0, 4):
                self.images.append(
                    [
                        False, pygame.image.load("sprites/enemy_transformer_launch"+str(i+1)+".gif").convert()
                    ]
                )

        self.image = self.images[0][1]
