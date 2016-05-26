import random

import pygame
from pygame import *
from src.enemy.unit import *


def create_enemies(surface, scroll_x):
    """ A function to create enemies

    Parameters:
        surface (pygame.Surface): the game screen
        scroll_x:

    Returns:
        pygame.sprites.Group : a group of enemies
    """
    enemies = pygame.sprite.Group()
    enemies.add(SitBot(scroll_x + 1250, 265, eid=2, animation_counter=15))
    enemies.add(SitBot(scroll_x + 2000, 360, eid=3, animation_counter=10))
    enemies.add(Giru(scroll_x + 1800, 460, eid=1, animation_counter=5))
    for i in range(4, 10):
        enemies.add(Moth(scroll_x + 1430, -50, eid=i, start_angle=180))
    enemies.add(Giru(scroll_x + 2700, 460, eid=11, animation_counter=5))
    enemies.add(Giru(scroll_x + 2900, 460, eid=12, animation_counter=5))
    enemies.add(Giru(scroll_x + 2800, 280, eid=13, animation_counter=10))
    enemies.add(Giru(scroll_x + 3000, 280, eid=14, animation_counter=10))
    for i in range(15, 21):
        enemies.add(Moth(scroll_x + 2340, 650, eid=i, start_angle=90))

    for i in range(21, 27):
        enemies.add(Moth(scroll_x + 3830, 650, eid=i, start_angle=90))

    for i in range(27, 37):
        enemies.add(Moth(scroll_x + 4370, -50, eid=i, start_angle=180))

    enemies.add(SitBot(scroll_x + 4370, 250, eid=37, animation_counter=15))
    enemies.add(SitBot(scroll_x + 4370, 455, eid=38, animation_counter=15))
    enemies.add(MissileBot(scroll_x + 5300, 465, eid=39, animation_counter=0))
    enemies.add(MissileBot(scroll_x + 5400, 465, eid=40, animation_counter=0))
    enemies.add(MissileBot(scroll_x + 5500, 465, eid=41, animation_counter=0))
    enemies.add(MissileBot(scroll_x + 5600, 465, eid=42, animation_counter=0))

    enemies.add(MissileBot(scroll_x + 3320, 465, eid=43, animation_counter=0))
    enemies.add(Boss(scroll_x + 6400, 250, eid=100, animation_counter=5))
    return enemies


def moth_group(scroll_x, enemy, eid, velocities, x0, step=-25, dir='SW'):
    """ A function that tells the group of moths to move a certain circular path

    Parameters:
        scroll_x:
        enemy:
        eid:
        velocities (list): a list of velocity sets in the x and y direction.
        x0 (int): initial x position
        step (int): time between each animation sequence
        dir (String): direction denoted by string - SW indicates southwest, NW indicates northwest

    """
    images = enemy.images
    if dir == 'NW':
        images = images[::-1]

    if x0+step < scroll_x < x0:
        if enemy.id == eid:
            if not images[3][0]:
                images[3][0] = True
                enemy.image = images[3][1]
            enemy.move(*velocities[0])  # asterisk unpacks the tuple i.e. (x, y) => x, y
    elif x0+(step*2) < scroll_x < x0+step:
        if enemy.id == eid:
            if not images[2][0]:
                images[2][0] = True
                enemy.image = images[2][1]
            enemy.move(*velocities[1])
    elif x0+(step*3) < scroll_x < x0+(step*2):
        if enemy.id == eid:
            if not images[1][0]:
                images[1][0] = True
                enemy.image = images[1][1]
            enemy.move(*velocities[2])
    elif x0+(step*4)-600 < scroll_x < x0+(step*3):
        if enemy.id == eid:
            if not images[0][0]:
                images[0][0] = True
                enemy.image = images[0][1]
            enemy.move(*velocities[3])

    x, y = enemy.rect.x, enemy.rect.y
    enemy.rect = enemy.image.get_rect() # update rect to fix moving hitboxes
    enemy.rect.x, enemy.rect.y = x, y


def boss_fight(boss_timer, player, enemy, projectiles):
    """ Boss AI. Not much of an AI. Moves in one single pattern.

    Parameters:
        boss_timer (int): a timer which the boss acts on
        player:
        enemy:
        projectiles:
    """
    if boss_timer % 50 == 0:
        beam = enemy.shoot(player.rect.x, player.rect.y)
        if beam:
            projectiles.add(beam)

    if boss_timer < 75:
        enemy.move(1, -2)
    elif 75 <= boss_timer < 150:
        enemy.move(-1, 2)
    elif 150 <= boss_timer < 200:
        enemy.move(-9, 0)
    elif 200 <= boss_timer < 225:
        enemy.move(3, -4)
    elif 225 <= boss_timer < 275:
        enemy.move(9, 0)
    elif 275 <= boss_timer < 300:
        enemy.move(-3, 4)


def load(scroll_x, boss_timer, player, enemies, projectiles):
    """ load the enemy script

    Parameters:
        scroll_x
        boss_timer (int): a timer which the boss acts on
        player
        enemies
        projectiles

    Returns:
        bool : if True, the game is over (victory)
    """
    for enemy in enemies:
        if enemy.id < 39 and scroll_x != 0 and scroll_x % (150+random.randint(0, 2)*25) == 0: # avoid bullet overflow when scroll_x = 0 (i.e. after unit dies)
            bullet = enemy.shoot(player.rect.x, player.rect.y)

            if bullet:
                projectiles.add(bullet)

        if 39 <= enemy.id < 44 and scroll_x % (100+random.randint(0, 2)*25) == 0:
            bullet = enemy.shoot(player.rect.x, player.rect.y)
            if bullet:
                projectiles.add(bullet)

        if -800 < scroll_x < -700:
            if enemy.id == 2:
                enemy.move(1, 0)
                
        velocities = [(-2, 5), (-4, 5), (-4, 2), (-4, 0)]
        for i in range(4, 10):
            moth_group(scroll_x, enemy, i, velocities, -650 + (i-4)*(-25), dir='SW')

        if -1200 < scroll_x < -900:
            if enemy.id == 1:
                enemy.move(-1, 0)

        if scroll_x == -1201:
            if enemy.id == 1:
                enemy.flip_sprite()
                enemy.pause()
        elif scroll_x == -1400:
            if enemy.id == 1:
                enemy.unpause()

        if -1500 < scroll_x < -1400:
            if enemy.id == 1:
                if scroll_x == -1499:
                    enemy.pause()
                else:
                    enemy.move(1, 0)

        if -2000 < scroll_x < -1800:
            if enemy.id == 11 or enemy.id == 12 or enemy.id == 13 or enemy.id == 14:
                if scroll_x == -1999:
                    enemy.pause()
                else:
                    enemy.move(-1, 0)

        velocities = [(-2, -7), (-4, -7), (-4, -3), (-4, 0)]
        for i in range(15, 21):
            moth_group(scroll_x, enemy, i, velocities, -1200 + (i-4)*(-25), dir='NW')

        velocities = [(-2, -7), (-4, -7), (-4, -3), (-4, 0)]
        for i in range(21, 27):
            moth_group(scroll_x, enemy, i, velocities, -2500 + (i-4)*(-25), dir='NW')
        #print(scroll_x)
        if -2500 < scroll_x < -2300:
            if enemy.id == 43:
                enemy.pause()
                enemy.siege_mode()

        velocities = [(-2, 8), (-4, 7), (-4, 2), (-4, 0)]
        for i in range(27, 37):
            moth_group(scroll_x, enemy, i, velocities, -3200 + (i-4)*(-25), dir='SW')

        if -4500 < scroll_x <= -4400:
            if enemy.id == 39:
                enemy.move(-1, 0)
        if -4600 < scroll_x <= -4500:
            if enemy.id == 39:
                enemy.pause()
                enemy.siege_mode()
            if enemy.id == 40:
                enemy.move(-1, 0)
        if -4700 < scroll_x <= -4600:
            if enemy.id == 40:
                enemy.pause()
                enemy.siege_mode()
            if enemy.id == 41:
                enemy.move(-1, 0)
        if -4800 < scroll_x <= -4700:
            if enemy.id == 41:
                enemy.pause()
                enemy.siege_mode()
            if enemy.id == 42:
                enemy.move(-1, 0)
        if -4900 < scroll_x <= -4800:
            if enemy.id == 42:
                enemy.pause()
                enemy.siege_mode()

        if scroll_x <= -5850:
            if enemy.id < 100:
                if not enemy.dead:
                    enemy.death(sound=False)

            if enemy.id == 100 and boss_timer != 0:
                if not enemy.dead:
                    if enemy.invincible:
                        enemy.invincible = False
                    boss_fight(boss_timer, player, enemy, projectiles)
                else:
                    pygame.mixer.music.fadeout(1000)
                    return True



