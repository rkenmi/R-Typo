import pygame
from pygame import *
import pytmx
from pytmx.util_pygame import load_pygame
from player import Player
from player_beam import PlayerWeapon
from block import Block
from icon import Icon
from player_beam_charged import PlayerWeaponCharged
from enemy_sitbot import SitBot
import sys
import random


def moth_group(scroll_x, enemy, eid, velocities, x0, step=-25, dir='SW'):
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


def enemy_script(scroll_x, boss_timer, player, enemies, projectiles):
    #print(scroll_x)
    for enemy in enemies:
        if enemy.id != 100 and scroll_x != 0 and scroll_x % 150 == 0: # avoid bullet overflow when scroll_x = 0 (i.e. after player dies)
            bullet = enemy.shoot(player.rect.x, player.rect.y)
            if bullet:
                projectiles.add(bullet)

        if -800 < scroll_x < -700:
            if enemy.id == 2:
                enemy.move(1, 0)
                if scroll_x % 30 == 0:
                    pass
                    #projectiles.add(enemy.shoot(player.rect.x, player.rect.y))

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

        if scroll_x <= -5850:
            if enemy.id == 100 and boss_timer != 0:
                if not enemy.dead:
                    if enemy.invincible:
                        enemy.invincible = False
                    boss_fight(boss_timer, player, enemy, projectiles)
                else:
                    pygame.mixer.music.fadeout(1000)
                    return True



