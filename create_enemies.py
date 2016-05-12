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
    enemies.add(Giru(2700, 460, eid=11, animation_counter=5))
    enemies.add(Giru(2900, 460, eid=12, animation_counter=5))
    enemies.add(Giru(2800, 280, eid=13, animation_counter=10))
    enemies.add(Giru(3000, 280, eid=14, animation_counter=10))
    return enemies
