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


def get_group(surface):
    enemies = pygame.sprite.Group()
    enemies.add(SitBot(700, 280, animation_timer=5))
    enemies.add(SitBot(1250, 265, animation_timer=15))
    enemies.add(SitBot(1400, 265, animation_timer=10))
    return enemies
