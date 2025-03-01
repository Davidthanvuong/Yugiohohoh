import pygame as pg
from pygame import Vector2 as vec
from pygame.event import peek as pgpeek
from typing import Optional as No
from abc import abstractmethod
from dataclasses import dataclass
from settings import *
tff = tuple[float, float]

CENTER = (NATIVE[0]//2, NATIVE[1]//2)
ZERO = (0, 0)
HALF = (0.5, 0.5)
ONE = (1, 1)
DEVELOPER = False

@dataclass
class MouseInfo:
    pos: vec
    clicked: bool
    host: No['Component']
    lastFocus: No['Component']

MOUSE = MouseInfo(vec(1, 0), False, None, None)

from .abstract_renderer import render, write
from .transform import Transform, Component
from .image import Image, Text
from .ui import IClickable
from .editor_inspector import DataField