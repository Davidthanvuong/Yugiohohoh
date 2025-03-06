import pygame as pg
from pygame import Vector2 as vec
from typing import Optional as No
RGB = tuple[int, int, int]
tff = tuple[float, float]
NoObj = No[object]


ALLOW_DEVELOPER = True
TOPLEFT = ZERO = (0, 0)
MIDTOP = (0.5, 0)
TOPRIGHT = (1, 0)

MIDLEFT = (0, 0.5)
CENTER = (0.5, 0.5)
MIDRIGHT = (1, 0.5)

BOTTOMLEFT = (0, 1)
MIDBOTTOM = (0.5, 1)
BOTTOMRIGHT = ONE = (1, 1)


class Mouse:
    pos = vec(1, 0)
    clicked = False
    hover: NoObj = None
    click: NoObj = None
    lastClick: NoObj = None
    focus: NoObj = None
 

class Color:
    black:      RGB = (0, 0, 0)
    dark:       RGB = (60, 60, 60)
    gray:       RGB = (100, 100, 100)
    light:      RGB = (180, 180, 180)
    white:      RGB = (255, 255, 255)

    forward:    RGB = (255, 50, 50)
    freedom:    RGB = (50, 255, 50)
    upward:     RGB = (50, 50, 255)
    
    relation:   RGB = (50, 150, 150)
    pivot:      RGB = (0, 255, 0)