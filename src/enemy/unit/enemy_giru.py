import pygame
from pygame.locals import *

from src.enemy.unit.enemy import Enemy

ANIMATION_STEP = 15 # time between each animation sprite


class Giru(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=70, animation_counter=0,
                 animation_step=10, dead_step=10):
        # Don't forget to call the super constructor
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max, animation_step, dead_step)

        # Enemy Configuration
        self.hp = 6
        self.can_shoot = True
        self.idle_animation = True
        self.stand_y = y - 14
        self.idle_y = y

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
            surface: Screen pygame object
        """
        if not self.dead: # enemy is alive
            stand = False
            self.animation_counter += 1

            if self.hit_animation: # enemy was hit with a beam
                self.hit_timer() # start hit timer

            if self.idle_animation:
                if self.animation_step > self.animation_counter >= 0: #  0-9
                    self.images[0][0] = True
                    self.image = self.images[0][1]
                elif self.animation_step * 3 > self.animation_counter >= self.animation_step: #  10-29
                    self.images[1][0] = True
                    self.image = self.images[1][1]
                    stand = True
                elif self.animation_step * 4 > self.animation_counter >= self.animation_step * 3:  # 30-39
                    self.images[2][0] = True
                    self.image = self.images[2][1]
                elif self.animation_step * 6 >= self.animation_counter >= self.animation_step * 4:  # 40-60
                    self.images[3][0] = True
                    self.image = self.images[3][1]
                    stand = True

                if stand:
                    self.rect.y = self.stand_y
                    stand = False
                else:
                    self.rect.y = self.idle_y

                x, y = self.rect.x, self.rect.y
                self.rect = self.image.get_rect() # update rect to fix moving hitboxes
                self.rect.x, self.rect.y = x, y

                if self.animation_counter >= self.animation_counter_max:
                    self.animation_counter = 0
                    for i in range(0, len(self.images)):
                        self.images[i][0] = False

            self.image.set_colorkey(pygame.Color(0, 0, 0))
            if not self.hit_animation:
                surface.blit(self.image, (self.rect.x, self.rect.y))
            else:
                surface.blit(self.image, (self.rect.x, self.rect.y), None, BLEND_RGBA_ADD)
        else: # enemy is about to die, start dead timer
            if self.dead_counter == 0 and not self.mute:
                self.death_sound.play()

            self.dead_counter += 2

            # enemy can't move while dead, but the animation must align with the scrolling screen
            self.move(-1, 0, bypass=True)

            for i in range(0, len(self.dead_images)):
                if (i+1)*self.dead_step < self.dead_counter < (i+2)*self.dead_step:
                    self.image = self.dead_images[i]

            self.image.set_colorkey(pygame.Color(0, 0, 0))
            if self.dead_counter < self.dead_counter_max:
                surface.blit(self.image, (self.rect.x, self.rect.y))

    def flip_sprite(self):
        if self.facing == 'left':
            self.facing = 'right'
        else:
            self.facing = 'left'

        self.load_images()

    def load_images(self):
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
            for i in range(0, 3):
                self.images.append(
                    [
                        False, pygame.image.load("sprites/enemy_giru"+str(i+1)+".gif").convert()
                    ]
                )
            self.images.append([False, pygame.image.load("sprites/enemy_giru2.gif").convert()])

        self.image = self.images[0][1]
