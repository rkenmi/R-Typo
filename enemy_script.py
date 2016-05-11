import pygame
from pygame import *
import pytmx
from pytmx.util_pygame import load_pygame
from player import Player
from player_beam import Beam
from block import Block
from icon import Icon
from player_beam_charged import ChargedBeam
from enemy_sitbot import SitBot
import sys


def moth_group(scroll_x, enemy, eid, x0, step=-25):
    if x0+step < scroll_x < x0:
        if enemy.id == eid:
            if not enemy.images[3][0]:
                enemy.images[3][0] = True
                enemy.image = enemy.images[3][1]
            enemy.move(-2, 5)
    elif x0+(step*2) < scroll_x < x0+step:
        if enemy.id == eid:
            if not enemy.images[2][0]:
                enemy.images[2][0] = True
                enemy.image = enemy.images[2][1]
            enemy.move(-4, 5)
    elif x0+(step*3) < scroll_x < x0+(step*2):
        if enemy.id == eid:
            if not enemy.images[1][0]:
                enemy.images[1][0] = True
                enemy.image = enemy.images[1][1]
            enemy.move(-4, 2)
    elif x0+(step*4)-600 < scroll_x < x0+(step*3):
        if enemy.id == eid:
            if not enemy.images[0][0]:
                enemy.images[0][0] = True
                enemy.image = enemy.images[0][1]
            enemy.move(-4, 0)

    x, y = enemy.rect.x, enemy.rect.y
    enemy.rect = enemy.image.get_rect() # update rect to fix moving hitboxes
    enemy.rect.x, enemy.rect.y = x, y


def enemy_script(scroll_x, game_time, player, enemies, projectiles):
    timer = 0
    for enemy in enemies:
        if scroll_x != 0 and scroll_x % 150 == 0: # avoid bullet overflow when scroll_x = 0 (i.e. after player dies)
            bullet = enemy.shoot(player.rect.x, player.rect.y)
            if bullet:
                projectiles.add(bullet)

        if -800 < scroll_x < -700:
            if enemy.id == 2:
                enemy.move(1, 0)
                if scroll_x % 50 == 0:
                    pass
                    #projectiles.add(enemy.shoot(player.rect.x, player.rect.y))

        for i in range(4, 10):
            moth_group(scroll_x, enemy, i, -650 + (i-4)*(-25))

        if -1200 < scroll_x < -900:
            if enemy.id == 1:
                enemy.move(-1, 0)

        if scroll_x == -1201:
            if enemy.id == 1:
                enemy.flip_sprite()
                enemy.pause()

        if scroll_x == -1249:
            if enemy.id == 1:
                enemy.unpause()

        if -1500 < scroll_x < -1250:
            if enemy.id == 1:
                enemy.move(1, 0)

