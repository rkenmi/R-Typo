import pygame

from src.player.weapon.player_beam import PlayerWeapon

CHARGE_STEP_TIME = 4


class PlayerWeaponCharged(PlayerWeapon):
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
        self.charge_image = None
        self.load_images()

        # Required for collision detection
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        # Charged beams will have varying damage
        self.charge_level = 0
        
        # Used as a timer for animation sequences
        self.animation_counter = 0

        # Used as a timer for duration of charge and charging animation sequences
        self.charge_counter = 0

        # Charged beams can fail (i.e. unit dies while charging), with no displayed output
        self.fail = 0
        
        # A flag to use up the charged shot if True
        self.shot_ready = False

    def move(self):
        """ Player 1 beam (lvl 1) moves only in the +x direction

        """
        if self.charge_level != 0:
            self.rect.x += self.vx
            if self.rect.x > self.oos_x:
                self.out_of_screen = True
        else:
            self.dead = True

    def draw(self, surface):
        """ Draws to screen

        Arguments:
            surface: Screen pygame object
        """
        charge_step = 9
        if not self.fail and self.charging:
            if not self.shot_ready:
                self.charge_sound.play(-1)

            self.charge_counter += 1
            self.shot_ready = True

            for i in range(0, len(self.charge_images)):
                if (charge_step*i) / (self.charge_level+1) <= self.charge_counter < (charge_step*(i+1)) / (self.charge_level+1):
                    self.charge_image = self.charge_images[i]
                    if i == 5:
                        self.charge_counter = 0
                        if self.charge_level < 6:
                            self.charge_level += 1
                            self.damage = self.charge_level * 3

            surface.blit(self.charge_image, (self.rect.x, self.rect.y - 20))
            self.charge_image.set_colorkey(pygame.Color(0, 0, 0))

        elif not self.fail and not self.charging: # key is let go, or beam is about to shoot
            self.charge_image = None
            self.animation_counter += 1

            if self.shot_ready:
                self.charge_sound.stop()
                self.charge_counter = 0
                self.shot_ready = False
                if self.charge_level > 0:
                    self.sound.play()
                if self.charge_level == 3:
                    self.rect.y -= 2
                elif self.charge_level == 4:
                    self.rect.y -= 5
                elif self.charge_level == 5:
                    self.rect.y -= 10
                elif self.charge_level == 6:
                    self.rect.y -= 15

            for i in range(0, 6):
                if self.charge_level == i+1:
                    if self.animation_counter % 3 == 0:
                        self.image = self.shoot_images[i][1]
                    else:
                        self.image = self.shoot_images[i][0]

            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect()  # update rect to fix moving hitboxes
            self.rect.x, self.rect.y = x, y

            #  Only trigger once, when drawn for the first time
            offset = 50  # make it "look" like the beam is actually traveling past the screen
            if self.oos_x == -1 and self.oos_y == -1:
                self.oos_x, self.oos_y = surface.get_width() - self.image.get_width() + offset, \
                                         surface.get_height() - self.image.get_height() + offset

            surface.blit(self.image, (self.rect.x, self.rect.y))
            self.image.set_colorkey(pygame.Color(0, 0, 0))

        elif self.fail:
            if self.shot_ready:
                self.charge_sound.stop()
                self.charge_counter = 0
                self.shot_ready = False

    def impact(self, surface):
        self.damage = 0  # prevent damage from triggering multiple times
        impact_step = 2

        if self.out_of_screen:
            self.dead = True
        elif not self.dead:
            self.impact_timer += 1
            for i in range(0, len(self.impact_images)):
                if i*impact_step < self.impact_timer < (i+1)*impact_step:
                    self.image = self.impact_images[i]

            x, y = self.rect.x, self.rect.y
            image = self.image
            image_x, image_y = self.image.get_width(), self.image.get_height()
            x += 10
            y -= 16
            if 3 <= self.charge_level < 6:
                x += 35
                y -= 14
                image = pygame.transform.scale(self.image, (image_x * 2, image_y * 2))
            elif self.charge_level == 6:
                x += 35
                y -= 32
                image = pygame.transform.scale(self.image, (image_x * 3, image_y * 3))

            if self.draw_impact and self.collide_distance > 100:  # only show impact if distance is far enough
                surface.blit(image, (x, y))

            if self.impact_timer > 6:
                self.dead = True

    def load_images(self):
        self.charge_images, self.shoot_images = [], []

        for i in range(0, 7):
            self.charge_images.append(pygame.image.load("sprites/player_wpn2_charge"+str(i+1)+".gif").convert())
            if i < 6:
                self.shoot_images.append(
                    (
                        pygame.image.load("sprites/player_wpn2_shoot"+str(i+1)+"a.gif").convert(),
                        pygame.image.load("sprites/player_wpn2_shoot"+str(i+1)+"b.gif").convert()
                    )
                )
                self.impact_images = []

        for i in range(0, 5):
            self.impact_images.append(pygame.image.load("sprites/player_wpn2_impact"+str(i+1)+".gif").convert())

        self.image = pygame.image.load("sprites/black.gif").convert() # temporary sprite
        self.charge_image = pygame.image.load("sprites/player_wpn1.gif").convert()