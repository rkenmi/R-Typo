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
        for i in range (0, 7):
            self.charge_images.append(pygame.image.load("sprites/player_wpn2_charge"+str(i+1)+".gif").convert())
            if i < 6:
                self.shoot_images.append(
                    (
                        pygame.image.load("sprites/player_wpn2_shoot"+str(i+1)+"a.gif").convert(),
                        pygame.image.load("sprites/player_wpn2_shoot"+str(i+1)+"b.gif").convert()
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

        # Charged beams will have varying damage
        self.damage = 0
        
        # Used as a timer for animation sequences
        self.animation_timer = 0

        # Used as a timer for duration of charge
        self.charge_timer = 0
        
        # A flag to use up the charged shot if True
        self.shot_ready = False

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface: Screen pygame object
        """
        charge_step = 9
        if not self.fail and self.charging:
            if not self.shot_ready:
                self.charge_sound.play(-1)

            self.charge_timer += 1
            self.shot_ready = True

            for i in range(0, len(self.charge_images)):
                if (charge_step*i) / (self.damage+1) <= self.charge_timer < (charge_step*(i+1)) / (self.damage+1):
                    self.charge_image = self.charge_images[i]
                    if i == 5:
                        self.charge_timer = 0
                        if self.damage < 6:
                            self.damage += 1

            surface.blit(self.charge_image, (self.rect.x, self.rect.y - 20))
            self.charge_image.set_colorkey(pygame.Color(0, 0, 0))

        elif not self.fail and not self.charging: # key is let go, or beam is about to shoot
            self.charge_image = None
            self.animation_timer += 1

            for i in range(0, 6):
                if self.damage == i+1:
                    if self.animation_timer % 3 == 0:
                        self.image = self.shoot_images[i][1]
                    else:
                        self.image = self.shoot_images[i][0]

            if self.shot_ready:
                self.charge_sound.stop()
                self.charge_timer = 0
                self.shot_ready = False

                if self.damage > 0:
                    self.sound.play()

                if self.damage == 3:
                    self.rect.y -= 2
                elif self.damage == 4:
                    self.rect.y -= 5
                elif self.damage == 5:
                    self.rect.y -= 10
                elif self.damage == 6:
                    self.rect.y -= 15

            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect() # update rect to fix moving hitboxes
            self.rect.x, self.rect.y = x, y

            surface.blit(self.image, (self.rect.x, self.rect.y))
            self.image.set_colorkey(pygame.Color(0, 0, 0))

        elif self.fail:
            if self.shot_ready:
                self.charge_sound.stop()
                self.charge_timer = 0
                self.shot_ready = False
