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
from enemy_moth import Moth
from enemy_giru import Giru
import sys


def get_group(surface):
    enemies = pygame.sprite.Group()
    enemies.add(SitBot(1250, 265, eid=2, animation_counter=15))
    enemies.add(SitBot(2000, 360, eid=3, animation_counter=10))
    enemies.add(Giru(1800, 460, eid=1, animation_counter=5))
    for i in range(4, 10):
        enemies.add(Moth(1430, -50, eid=i))
    return enemies
