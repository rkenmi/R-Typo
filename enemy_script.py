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


def enemy_script(scroll_x, enemies):
    if -700 < scroll_x < -500:
        for enemy in enemies:
            if enemy.id == 2:
                enemy.move(-1, 0)