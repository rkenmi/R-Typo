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
from enemy_moth import Moth
from enemy_giru import Giru
from enemy_boss import Boss
import sys


def get_group(surface, scroll_x):
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

    enemies.add(Boss(scroll_x + 6400, 250, eid=100, animation_counter=5))
    return enemies
