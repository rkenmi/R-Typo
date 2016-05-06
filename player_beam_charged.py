import pygame
import math
from player_beam import Beam
from pygame.locals import *

CHARGE_STEP_TIME = 4


class ChargedBeam(Beam):
    def __init__(self, x, y):
        """ Creates a beam (level 1)

        Arguments:
            x (int) : x coordinate of screen
            y (int) : y coordinate of screen
            vx (int) : velocity in x-direction of ball
            vy (int) : velocity in y-direction of ball
        """
        # Don't forget to call the super constructor
        super().__init__(x, y, play_sound=False)

        self.charge_sound = pygame.mixer.Sound(file="sounds/player_wpn2_charge1.ogg")
        self.sound = pygame.mixer.Sound(file="sounds/player_wpn2_shoot.ogg")

        # Load images
        self.charge_images, self.shoot_images = [], []
        for i in range (1, 8):
            self.charge_images.append(pygame.image.load("sprites/player_wpn2_charge"+str(i)+".gif").convert())
            if i < 6:
                self.shoot_images.append(
                    (
                    pygame.image.load("sprites/player_wpn2_shoot"+str(i)+"a.gif").convert(),
                    pygame.image.load("sprites/player_wpn2_shoot"+str(i)+"b.gif").convert()
                     )
                )

        self.image = pygame.image.load("sprites/black.gif").convert() # temporary sprite

        self.charge_image = self.charge_images[0]
        #self.image = pygame.image.load("sprites/player_wpn2_shoot5a.gif").convert() # temporary sprite

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))
        self.charge_image.set_colorkey(pygame.Color(0, 0, 0))

        # Required for collision detection
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        # Charged beams have multiple charge levels
        self.charge_level = 0
        
        # Used as a timer for animation sequences
        self.animation_timer = 0

        # Used as a timer for duration of charge
        self.charge_timer = 0
        
        # A flag to use up the charged shot if True
        self.shot_ready = False



    def draw(self, SCREEN):
        """ Draws to screen

        Arguments:
            SCREEN: Screen pygame object
        """
        charge_step = 10
        if self.charging:
            if not self.shot_ready:
                self.charge_sound.play(-1)

            self.charge_timer += 1
            self.shot_ready = True

            if 0 <= self.charge_timer < charge_step / (self.charge_level+1):
                self.charge_image = self.charge_images[1]
            elif charge_step / (self.charge_level+1) < self.charge_timer < charge_step*2 / (self.charge_level+1):
                self.charge_image = self.charge_images[2]
            elif charge_step*2 / (self.charge_level+1) < self.charge_timer < charge_step*3 / (self.charge_level+1):
                self.charge_image = self.charge_images[3]
            elif charge_step*3 / (self.charge_level+1) < self.charge_timer < charge_step*4 / (self.charge_level+1):
                self.charge_image = self.charge_images[4]
            elif charge_step*4 / (self.charge_level+1) < self.charge_timer < charge_step*5 / (self.charge_level+1):
                self.charge_image = self.charge_images[5]
            elif charge_step*5 / (self.charge_level+1) < self.charge_timer < charge_step*6 / (self.charge_level+1):
                self.charge_image = self.charge_images[6]
                if self.charge_level < 6:
                    self.charge_level += 1

                self.charge_timer = 0
            SCREEN.blit(self.charge_image, (self.rect.x, self.rect.y - 20))
            self.charge_image.set_colorkey(pygame.Color(0, 0, 0))

        else: # key is let go, or beam is about to shoot
            self.charge_image = None
            self.animation_timer += 1
            if self.charge_level == 1:
                if self.animation_timer % 3 == 0:
                    self.image = self.shoot_images[0][1]
                else:
                    self.image = self.shoot_images[0][0]
            elif self.charge_level == 2:
                if self.animation_timer % 3 == 0:
                    self.image = self.shoot_images[1][1]
                else:
                    self.image = self.shoot_images[1][0]
            elif self.charge_level == 3:
                if self.animation_timer % 3 == 0:
                    self.image = self.shoot_images[2][1]
                else:
                    self.image = self.shoot_images[2][0]
            elif self.charge_level == 4:
                if self.animation_timer % 3 == 0:
                    self.image = self.shoot_images[2][1]
                else:
                    self.image = self.shoot_images[2][0]
            elif self.charge_level == 5:
                if self.animation_timer % 3 == 0:
                    self.image = self.shoot_images[3][1]
                else:
                    self.image = self.shoot_images[3][0]
            elif self.charge_level == 6:
                if self.animation_timer % 3 == 0:
                    self.image = self.shoot_images[4][1]
                else:
                    self.image = self.shoot_images[4][0]

            if self.shot_ready:
                self.charge_sound.stop()
                self.charge_timer = 0
                self.shot_ready = False

                if self.charge_level > 0:
                    self.sound.play()

                if self.charge_level == 3:
                    self.rect.y -= 2
                elif self.charge_level == 4:
                    self.rect.y -= 5
                elif self.charge_level == 5:
                    self.rect.y -= 10
                elif self.charge_level == 6:
                    self.rect.y -= 15

            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect() # fixes clipping issue with charged beam sprites
            self.rect.x, self.rect.y = x, y

            SCREEN.blit(self.image, (self.rect.x, self.rect.y))
            self.image.set_colorkey(pygame.Color(0, 0, 0))