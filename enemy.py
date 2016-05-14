import pygame
import math
from pygame.locals import *
from enemy_bullet import EnemyWeapon


ANIMATION_STEP = 15 # time between each animation sprite
ANIMATION_COUNTER_MAX = 200 # time after which animation is looped (back to the starting animation)
DEAD_STEP = 10 # time between each death sprite
DEAD_COUNTER_MAX = 70 # time after which


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, eid=0, animation_counter_max=ANIMATION_COUNTER_MAX, dead_counter_max=DEAD_COUNTER_MAX
                 , animation_step=ANIMATION_STEP, dead_step=DEAD_STEP):
        # Don't forget to call the super constructor
        super().__init__()

        # Enemy Configuration
        self.id = eid  # enemy id used in scripting
        self.hp = 1  # default 1 hp
        self.dead = False
        self.can_shoot = True
        self.mute = False  # mute death sound
        self.idle_animation = True
        self.facing = 'left'
        self.invincible = False

        # Load default images
        self.image = pygame.image.load("sprites/black.gif").convert()  # temporary sprite
        self.images, self.dead_images = [], []
        self.load_images()
        self.load_dead_images()

        # Sounds
        self.death_sound = pygame.mixer.Sound('sounds/enemy_dead.wav')

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Used as a timer for animation sequences
        self.animation_step, self.dead_step = animation_step, dead_step
        self.animation_counter, self.dead_counter = 0, 0
        self.animation_counter_max, self.dead_counter_max = animation_counter_max, dead_counter_max
        self.hit_counter = 0
        self.hit_animation = False
        self.out_of_screen = False

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface: Screen pygame object
        """
        if not self.dead: # enemy is alive
            self.animation_counter += 1
            
            if self.hit_animation: # enemy was hit with a beam
                self.hit_timer() # start hit timer

            if self.idle_animation:
                for i in range(0, len(self.images)+1):
                    if i == len(self.images) and self.animation_counter > (i+1)*self.animation_step:
                        self.image = self.images[0][1]
                    elif self.animation_counter > (i+1)*self.animation_step and not self.images[i][0]:
                        self.images[i][0] = True
                        self.image = self.images[i][1]

                if self.animation_counter > self.animation_counter_max:
                    self.animation_counter = 0
                    for i in range(0, len(self.images)):
                        self.images[i][0] = False

            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect() # update rect to fix moving hitboxes
            self.rect.x, self.rect.y = x, y

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

            if self.dead_counter < self.dead_counter_max:
                self.image.set_colorkey(pygame.Color(0, 0, 0))
                surface.blit(self.image, (self.rect.x, self.rect.y))

    def death(self, sound=True):
        self.dead = True
        self.can_shoot = False
        if not sound:
            self.mute = True

    def shoot(self, target_x, target_y, charged=False):
        """ The enemy shoots some projectile at the player. Some enemies can do this, others can't.

        Arguments:
            target_x (int): x coordinate of the aimed location
            target_y (int): y coordinate of the aimed location
            charged (bool): True/False depending on whether it is a charged beam or not

        Returns:
            A newly created EnemyWeapon object
        """
        if self.facing == 'right':
            if self.can_shoot and -800 < self.rect.x - target_x < 0:
                return EnemyWeapon(self.rect.x + self.image.get_width(), self.rect.y, target_x, target_y)

        elif self.facing == 'left':
            if self.can_shoot and 0 < self.rect.x - target_x < 800:
                return EnemyWeapon(self.rect.x, self.rect.y, target_x, target_y)

    def move(self, x, y, bypass=False):
        """ Moves the enemy if enemy is not dead.

        Arguments:
            x (int): x coord to move
            y (int): y coord to move
            bypass (bool) : if bypass is True, allow movement even when the enemy is dead
        """
        if self.dead_counter == 0 or bypass:
            self.rect.x += x
            self.rect.y += y

    def hit_timer(self):
        """ If Enemy is hit, start the hit timer which will cause it to give a flashing animation
        handled by .draw().

        Arguments:
            x (int): x coord to move
            y (int): y coord to move
        """
        self.hit_counter += 1
        if self.hit_counter > 5:
            self.hit_counter = 0
            self.hit_animation = False

    def take_damage(self, damage):
        """ Enemy takes damage, losing HP. If HP falls to 0 or lower, the enemy dies.

        Parameters:
            damage (int) : Integer amount that the enemy takes as damage
        """
        self.hp -= damage
        if self.hp <= 0:
            self.death()
        elif not self.hit_animation:
            self.hit_animation = True

    def pause(self):
        self.idle_animation = False

    def unpause(self):
        self.idle_animation = True

    def flip_sprite(self):
        pass

    def load_images(self):
        pass

    def load_dead_images(self):
        self.dead_images = []
        for i in range(0, 6):
            self.dead_images.append(pygame.image.load("sprites/enemy_dead"+str(i+1)+".gif").convert())
