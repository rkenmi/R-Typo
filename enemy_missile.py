import pygame
from enemy_bullet import EnemyWeapon
import math

ANIMATION_STEP = 3


#  Derive your class from the Sprite super class
class EnemyWeaponMissile(EnemyWeapon):
    def __init__(self, x, y, t1, target_x=0, target_y=0, play_sound=True, random_aim=0):
        """ Creates a circular red bullet used by regular mobs/enemies

        Arguments:
            x (int) : x coordinate of screen
            y (int) : y coordinate of screen
            vx (int) : velocity in x-direction of ball
            vy (int) : velocity in y-direction of ball
        """
        # Don't forget to call the super constructor
        super().__init__(x, y, target_x, target_y, play_sound);

        self.random_aim = random_aim
        # Load image
        self.shoot_images = []
        self.load_images()

        self.animation_counter = 0
        #self.move_counter
        self.x0, self.y0 = x, y
        self.t1 = t1

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface: Screen pygame object
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
        """ Player 1 beam (lvl 1) moves only in the +x direction

        Arguments:
            x (int) : x coordinate to move
            y (int) : y coordinate to move
            surface (pygame.Surface) : the screen to display
        """
        t = self.animation_counter

        if 0 <= t < 50+self.random_aim:
            self.rect.x -= 1
            self.rect.y -= math.sqrt(math.sqrt(math.fabs(50 - t)))
        else:  # negative
            self.rect.x -= 1
            self.rect.y += math.sqrt(math.sqrt(math.fabs(t - 50)))

    def load_images(self):
        self.shoot_images = []
        for i in range(0, 7):
            if i == 2:
                self.shoot_images.append(pygame.image.load("sprites/enemy_transformer_wpn_135.gif").convert())
            if i == 5:
                self.shoot_images.append(pygame.image.load("sprites/enemy_transformer_wpn_225.gif").convert())
            self.shoot_images.append(pygame.image.load("sprites/enemy_transformer_wpn_"+str(i*30 + 90)+".gif").convert())
        self.image = self.shoot_images[0]
        #self.image = pygame.image.load("sprites/player_wpn2_shoot6a.gif").convert()

