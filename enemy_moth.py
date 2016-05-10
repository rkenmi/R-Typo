import pygame
from enemy import Enemy


class Moth(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=70, animation_counter=0):
        # Don't forget to call the super constructor
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max)

        # Load images
        self.images = []
        for i in range(0, 4):
            if i == 2:
                self.images.append([False, pygame.image.load("sprites/enemy_moth_225.gif").convert()])
            self.images.append(
                [
                    False, pygame.image.load("sprites/enemy_moth_"+str(i*30+180)+".gif").convert()
                ]
            )
        self.image = self.images[4][1]

        # Set the color that should be transparent
        self.image.set_colorkey(pygame.Color(0, 0, 0))

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Variables
        self.hp = 3
        self.can_shoot = False  # Does not shoot!
        # Used as a timer for animation sequences
        self.animation_counter = animation_counter
        self.idle_animation = False

        print(self.id)
    #def draw(self, surface):
    #    surface.blit(self.image, (self.rect.x, self.rect.y))