import pygame
import math
from player_beam import Beam
from pygame.locals import *


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
        self.charge_timer = 0

        # Load image
        self.image = pygame.image.load("sprites/black.gif").convert()
        self.charge_image = pygame.image.load("sprites/player_wpn2_charge1.gif").convert()

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))
        self.charge_image.set_colorkey(pygame.Color(0, 0, 0))

        # Required for collision detection
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.vx = 15
        self.out_of_screen = False
        self.charging = False
        self.charge_level = 0
        self.animation_loop = 0
        self.shot_ready = False


    def draw(self, SCREEN):
        """ Draws to screen

        Arguments:
            SCREEN: Screen pygame object
        """
        if self.charging:
            if not self.shot_ready:
                self.charge_sound.play(-1)
               #self.charge_sound.play()

            self.charge_timer += 1
            self.shot_ready = True
            print(self.charge_level)
            if 0 <= self.charge_timer < 4:
                self.charge_image = pygame.image.load("sprites/player_wpn2_charge2.gif").convert()
            elif 4 < self.charge_timer < 8:
                self.charge_image = pygame.image.load("sprites/player_wpn2_charge3.gif").convert()
            elif 8 < self.charge_timer < 12:
                self.charge_image = pygame.image.load("sprites/player_wpn2_charge4.gif").convert()
            elif 12 < self.charge_timer < 16:
                self.charge_image = pygame.image.load("sprites/player_wpn2_charge5.gif").convert()
            elif 16 < self.charge_timer < 20:
                self.charge_image = pygame.image.load("sprites/player_wpn2_charge6.gif").convert()
            elif 20 < self.charge_timer < 24:
                self.charge_image = pygame.image.load("sprites/player_wpn2_charge7.gif").convert()
                if self.charge_level < 6:
                    self.charge_level += 1

                self.charge_timer = 0
            SCREEN.blit(self.charge_image, (self.rect.x, self.rect.y - 20))
            self.charge_image.set_colorkey(pygame.Color(0, 0, 0))

        else: # key is let go, or beam is about to shoot
            if self.shot_ready:
                self.charge_sound.stop()
                self.charge_timer = 0
                self.shot_ready = False
                if self.charge_level > 0:
                    self.sound.play()

            self.animation_loop += 1
            if self.charge_level == 1:
                if self.animation_loop % 3 == 0:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot1b.gif").convert()
                else:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot1a.gif").convert()
            elif self.charge_level == 2:
                if self.animation_loop % 3 == 0:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot2b.gif").convert()
                else:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot2a.gif").convert()
            elif self.charge_level == 3:
                if self.animation_loop % 3 == 0:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot3b.gif").convert()
                else:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot3a.gif").convert()
            elif self.charge_level == 4:
                if self.animation_loop % 3 == 0:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot4b.gif").convert()
                else:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot4a.gif").convert()
            elif self.charge_level == 5:
                if self.animation_loop % 3 == 0:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot4b.gif").convert()
                else:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot4a.gif").convert()
            elif self.charge_level == 6:
                if self.animation_loop % 3 == 0:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot5b.gif").convert()
                else:
                    self.image = pygame.image.load("sprites/player_wpn2_shoot5a.gif").convert()

            if self.charge_level < 3:
                SCREEN.blit(self.image, (self.rect.x, self.rect.y))
            elif self.charge_level == 3:
                SCREEN.blit(self.image, (self.rect.x, self.rect.y - 2))
            elif self.charge_level == 4:
                SCREEN.blit(self.image, (self.rect.x, self.rect.y - 5))
            elif self.charge_level == 5:
                SCREEN.blit(self.image, (self.rect.x, self.rect.y - 10))
            elif self.charge_level == 6:
                SCREEN.blit(self.image, (self.rect.x, self.rect.y - 15))

            self.image.set_colorkey(pygame.Color(0, 0, 0))


    def bounce(self):
        """ Bounces the ball by inverting the angles.
        """
        if self.hit is False: # sort of helps with collision/stuck issues when balls hit each other
            magnitude = math.sqrt(math.pow(self.vy, 2) + math.pow(self.vx, 2))
            theta = math.atan2(self.vy, self.vx) # get velocity direction
            theta += math.pi/2 # flip the velocity direction
            self.vx = math.cos(theta) * magnitude
            self.vy = math.sin(theta) * magnitude

        self.hit = not self.hit


    def move(self, SCREEN):
        """ Player 1 beam (lvl 1) moves only in the +x direction

        Arguments:
            x (int): x coord to move
            y (int): y coord to move
        """
        #r_collide = self.rect.x + self.image.get_width() + self.vx > SCREEN.get_width()
        #l_collide = self.rect.x + self.vx < 0
        #t_collide = self.rect.y + self.vy < 0
        #b_collide = self.rect.y + self.image.get_height() + self.vy > SCREEN.get_height()

        # Check collision on right and left sides of screen
        #if l_collide or r_collide:
        #    self.vx *= -1

        # Check collision on top and bottom sides of screen
        #if t_collide or b_collide:
        #    self.vy *= -1

        self.rect.x += self.vx
        if self.rect.x > SCREEN.get_width():
            self.out_of_screen = True