import pygame
import math
from pygame.locals import *


ANIMATION_STEP = 15 # time between each animation sprite
ANIMATION_TIMER_MAX = 200 # time after which animation is looped (back to the starting animation)
DEAD_STEP = 10 # time between each death sprite
DEAD_TIMER_MAX = 70 # time after which


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, eid=0, animation_timer_max=ANIMATION_TIMER_MAX, dead_timer_max=DEAD_TIMER_MAX):
        # Don't forget to call the super constructor
        super().__init__()

        self.image = pygame.image.load("sprites/black.gif").convert() # temporary sprite

        # Load default images
        self.images = []
        self.dead_images = []
        for i in range(0, 6):
            self.dead_images.append(pygame.image.load("sprites/enemy_dead"+str(i+1)+".gif").convert())

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))

        # Sounds
        self.death_sound = pygame.mixer.Sound('sounds/player_dead.ogg')

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Variables
        self.id = eid
        self.hp = 1 # default 1 hp
        self.dead = False
        self.mute = False # mute death sound

        # Used as a timer for animation sequences
        self.animation_timer, self.dead_timer = 0, 0
        self.animation_timer_max, self.dead_timer_max = animation_timer_max, dead_timer_max
        self.hit_timer = 0
        self.hit_animation = False
        self.out_of_screen = False

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface: Screen pygame object
        """
        if not self.dead:
            self.animation_timer += 1

            ##### Got Hit! animation #####
            self.draw_hit_timer()

            for i in range(0, len(self.images)+1):
                if i == len(self.images) and self.animation_timer > (i+1)*ANIMATION_STEP:
                    self.image = self.images[0][1]
                elif self.animation_timer > (i+1)*ANIMATION_STEP and not self.images[i][0]:
                    self.images[i][0] = True
                    self.image = self.images[i][1]

            if self.animation_timer > self.animation_timer_max:
                self.animation_timer = 0
                for i in range(0, len(self.images)):
                    self.images[i][0] = False

            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect() # update rect to fix moving hitboxes
            self.rect.x, self.rect.y = x, y

            if not self.hit_animation:
                surface.blit(self.image, (self.rect.x, self.rect.y))
            else:
                surface.blit(self.image, (self.rect.x, self.rect.y), None, BLEND_RGB_ADD)
        else:
            if self.dead_timer == 0 and not self.mute:
                self.death_sound.play()

            self.dead_timer += 2

            for i in range(0, len(self.dead_images)):
                if (i+1)*DEAD_STEP < self.dead_timer < (i+2)*DEAD_STEP:
                    self.image = self.dead_images[i]

            if self.dead_timer < self.dead_timer_max:
                surface.blit(self.image, (self.rect.x, self.rect.y))

    def death(self, sound=True):
        self.dead = True
        if not sound:
            self.mute = True

    def shoot(self, beam_x, beam_y, charged=False):
        """
        Arguments:
            beam_x (int): x coordinate of where beam will be drawn
            beam_y (int): y coordinate of where beam will be drawn
            charged (bool): True/False depending on whether it is a charged beam or not

        Returns:
            A newly created beam object
        """
        """
        if not charged:
            b = Beam(beam_x, beam_y)
        else:
            b = ChargedBeam(beam_x, beam_y)
            b.charging = True
            self.charged_beam = b
        return b
        """
        pass

    def move(self, x, y):
        """ Moves the enemy. Very barebones.

        Arguments:
            x (int): x coord to move
            y (int): y coord to move
        """
        self.rect.x += x
        self.rect.y += y

    def draw_hit_timer(self):
        """ If Enemy is hit, start the hit timer which will cause it to give a flashing animation
        handled by .draw(). This function does not actually draw anything, but it is a helper
        function for .draw().

        Arguments:
            x (int): x coord to move
            y (int): y coord to move
        """
        if self.hit_animation:
            self.hit_timer += 1
            if self.hit_timer > 5:
                self.hit_timer = 0
                self.hit_animation = False

    def take_damage(self, damage):
        """ Enemy takes damage, losing 1 HP.

        Parameters:
            damage (int) : Integer amount that the

        """
        #print(damage)
        self.hp -= damage
        if self.hp <= 0:
            self.death()
        elif not self.hit_animation:
            self.hit_animation = True
