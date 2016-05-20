import pygame

from src.enemy.unit.enemy import Enemy


class SitBot(Enemy):
    def __init__(self, x, y, eid=0, animation_counter_max=60, dead_counter_max=70, animation_counter=0):
        # Don't forget to call the super constructor
        super().__init__(x, y, eid, animation_counter_max, dead_counter_max)

        # Load images
        self.images = []
        self.load_images()

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Enemy Configuration
        self.hp = 15

        # Used as a timer for animation sequences
        self.animation_counter = animation_counter

    def load_images(self):
        self.images = []
        for i in range(0, 3):
            self.images.append(
                [
                    False,
                    pygame.image.load("sprites/enemy_sitbot_stand"+str(i+1)+".gif").convert()
                ]
            )
        self.image = self.images[0][1]
