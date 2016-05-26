import pygame

from src.enemy.weapon.enemy_wpn import EnemyWeapon

ANIMATION_STEP = 3


#  Derive your class from the Sprite super class
class EnemyWeaponBeam(EnemyWeapon):
    def __init__(self, x, y, target_x, target_y, play_sound=True, random_aim=0):
        """ Creates a circular red bullet used by regular mobs/enemies

        Arguments:
            x (int) : x coordinate of screen
            y (int) : y coordinate of screen
            target_x (int) : x coordinate of target on screen
            target_y (int) : y coordinate of target on screen
            play_sound (bool) : if True, play sound of the weapon. (Not implemented yet)
            random_aim (int) : gives the weapon a random offset to the y-distance
        """
        # Don't forget to call the super constructor
        super().__init__(x, y, target_x, target_y, play_sound)

        self.random_aim = random_aim
        # Load image
        self.shoot_images = []
        self.load_images()

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface (pygame.Surface) : the game screen
        """
        self.animation_counter += 1

        for i in range(0, len(self.shoot_images)):
            if self.animation_counter > (i+1)*ANIMATION_STEP:
                self.image = self.shoot_images[i]

        if self.animation_counter > ANIMATION_STEP * 3:
            self.animation_counter = 0

        surface.blit(self.image, (self.rect.x - 15, self.rect.y))
        self.move()

    def move(self):
        """ Player 1 beam (lvl 1) moves only in the +x direction

        Arguments:
            x (int) : x coordinate to move
            y (int) : y coordinate to move
            surface (pygame.Surface) : the game screen
        """
        self.rect.x = self.rect.x - 4
        self.rect.y = self.rect.y + self.random_aim
        #self.rect.y = self.y0 + self.y1 * self.move_counter
        self.move_counter += 2
        if self.rect.x < self.oos_x or self.rect.y < self.oos_y:
            self.out_of_screen = True

    def load_images(self):
        """ A simple method that loads all images for future use.

        """
        self.shoot_images = []
        for i in range(0, 3):
            self.shoot_images.append(pygame.image.load("sprites/enemy_boss_wpn2_shoot"+str(i+1)+".gif").convert())
        self.image = self.shoot_images[0]