import pygame, random
from enemy import Enemy
from pygame.locals import *
from enemy_beam import EnemyWeaponBeam

ANIMATION_STEP = 15 # time between each animation sprite


class Boss(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=60, animation_counter=0,
                 animation_step=10, dead_step=10):
        # Don't forget to call the super constructor
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max, animation_step, dead_step)

        # Enemy Configuration
        self.hp = 120
        self.can_shoot = True
        self.idle_animation = True
        self.stand_y = y - 14
        self.idle_y = y
        self.invincible = True

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

    def shoot(self, target_x, target_y, charged=False):
        """ The enemy shoots some projectile at the player. Some enemies can do this, others can't.

        Arguments:
            target_x (int): x coordinate of the aimed location
            target_y (int): y coordinate of the aimed location
            charged (bool): True/False depending on whether it is a charged beam or not

        Returns:
            A newly created Bullet object
        """

        if self.can_shoot and 0 < self.rect.x - target_x < 800:
            pygame.mixer.Sound(file="sounds/player_wpn2_shoot.ogg").play()
            return EnemyWeaponBeam(self.rect.x, self.rect.y, target_x, target_y, random_aim=random.randint(-1, 1))


    def move(self, x, y, bypass=False):
        """ Moves the enemy if enemy is not dead.

        Arguments:
            x (int): x coord to move
            y (int): y coord to move
            bypass (bool) : if bypass is True, allow movement even when the enemy is dead
        """
        if self.dead_counter == 0 or bypass:
            if x > 0:
                self.image = self.images[0][1]
            else:
                self.image = self.images[1][1]

            self.rect.x += x
            self.rect.y += y

    def flip_sprite(self):
        if self.facing == 'left':
            self.facing = 'right'
        else:
            self.facing = 'left'

        self.load_images()

    def load_images(self):
        self.images = []

        for i in range(0, 3):
            self.images.append(
                [
                    False, pygame.image.load("sprites/enemy_boss"+str(i+1)+".gif").convert()
                ]
            )
        self.images.append([False, pygame.image.load("sprites/enemy_giru2.gif").convert()])

        self.image = self.images[0][1]
