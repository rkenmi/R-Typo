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


def enemy_script(scroll_x, player, enemies, projectiles):
    for enemy in enemies:
        if scroll_x != 0 and scroll_x % 150 == 0: # avoid bullet overflow when scroll_x = 0 (i.e. after player dies)
            bullet = enemy.shoot(player.rect.x, player.rect.y)
            if bullet:
                projectiles.add(bullet)

    if -600 < scroll_x < -500:
        for enemy in enemies:
            if enemy.id == 2:
                enemy.move(-1, 0)
                if scroll_x % 50 == 0:
                    pass
                    #projectiles.add(enemy.shoot(player.rect.x, player.rect.y))