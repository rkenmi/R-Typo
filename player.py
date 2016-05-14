import pygame
import math
from player_beam import PlayerWeapon
from player_beam_charged import PlayerWeaponCharged
from pygame.locals import *

#Derive your class from the Sprite super class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """ Creates a ball

        Arguments:
            x (int) : x coordinate of screen
            y (int) : y coordinate of screen
            vx (int) : velocity in x-direction of ball
            vy (int) : velocity in y-direction of ball
        """
        # Don't forget to call the super constructor
        super().__init__();

        # Load images
        self.image = pygame.image.load("sprites/player.gif").convert()
        self.dead_images = []
        self.load_images()

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mask = pygame.mask.from_surface(self.image, 0)
        #print(self.mask.outline())
        # Position to respawn at
        self.respawn_pos = (x, y)
        self.last_pos = (0, 0) # for wall collision

        # 'E' key beam, or charged beam
        self.charged_beam = None

        # Variables
        self.dead = False
        self.dead_timer = 0
        self.invincible = False
        self.invincible_timer = 0

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface: Screen pygame object
        """
        if not self.dead and not self.invincible:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        elif not self.dead and self.invincible:
            self.invincible_timer += 1

            if self.invincible_timer % 5 == 0:
                surface.blit(self.image, (self.rect.x, self.rect.y))

            if self.invincible_timer > 90:
                self.invincible = False
                self.invincible_timer = 0
        else:
            if self.dead_timer == 0:
                pygame.mixer.Sound('sounds/player_dead.ogg').play()

            self.dead_timer += 1

            death_step = 5
            for i in range(0, len(self.dead_images)):
                if (i+1)*death_step < self.dead_timer < (i+2)*death_step:
                    self.image = self.dead_images[i]

            self.rect.x -= 1
            if self.dead_timer < 35:
                surface.blit(self.image, (self.rect.x, self.rect.y))

    def death(self):
        self.dead = True
        if self.charged_beam:
            self.charged_beam.fail = True
            self.charged_beam.charge_sound.stop()

    def respawn(self):
        self.rect.x = self.respawn_pos[0]
        self.rect.y = self.respawn_pos[1]
        self.dead = False
        self.dead_timer = 0
        self.invincible = True

        # Revert original sprite
        self.image = pygame.image.load("sprites/player.gif").convert()
        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))

    def shoot(self, beam_x, beam_y, charged=False):
        """
        Arguments:
            beam_x (int): x coordinate of where beam will be drawn
            beam_y (int): y coordinate of where beam will be drawn
            charged (bool): True/False depending on whether it is a charged beam or not

        Returns:
            A newly created beam object
        """
        if not charged:
            b = PlayerWeapon(beam_x, beam_y)
        else:
            b = PlayerWeaponCharged(beam_x, beam_y)
            b.charging = True
            self.charged_beam = b
        return b

    def move(self, surface, x, y, bypass_wall=False):
        """ Moves the beam by altering the x and y coordinates.

        Arguments:
            x (int): x coord to move
            y (int): y coord to move
        """

        if self.dead is False:
            r_collide = self.rect.x + self.image.get_width() > surface.get_width()
            l_collide = self.rect.x < 0
            t_collide = self.rect.y < 0
            b_collide = self.rect.y + self.image.get_height() > surface.get_height() - 40

            if bypass_wall:
                self.rect.x += x
                self.rect.y += y
            else:
                if not ((r_collide and x > 0) or (l_collide and x < 0)):
                    self.rect.x += x
                    if self.charged_beam:
                        self.charged_beam.rect.x += x

                if not ((t_collide and y < 0) or (b_collide and y > 0)):
                    self.rect.y += y
                    if self.charged_beam:
                        self.charged_beam.rect.y += y

    def load_images(self):
        self.image = pygame.image.load("sprites/player.gif").convert()
        self.dead_images = []
        for i in range(0, 6):
            self.dead_images.append(pygame.image.load("sprites/player_dead"+str(i+1)+".gif").convert())

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))
