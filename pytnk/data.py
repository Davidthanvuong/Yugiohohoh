import pygame as pg
from pygame import Vector2 as vec
RGB = tuple[int, int, int]
RGBA = tuple[int, int, int, int]
tff = tuple[float, float]

TOPLEFT = ZERO = (0, 0)
MIDTOP = (0.5, 0)
TOPRIGHT = (1, 0)

MIDLEFT = (0, 0.5)
CENTER = (0.5, 0.5)
MIDRIGHT = (1, 0.5)

BOTTOMLEFT = (0, 1)
MIDBOTTOM = (0.5, 1)
BOTTOMRIGHT = ONE = (1, 1)

FORWARD = vec(1, 0)
UPWARD = vec(0, -1)
HALF_RADIAN = 1.57
vZERO = vec(0, 0)
vONE = vec(1, 1)

EMPTY = BACK = False
OCCUPIED = FRONT = True

class App:
    running = True
    debugMode = True
    targetFPS = 60
    screen: pg.Surface

    fpsTrackDur = 1.0
    native = (1400, 1000)
    vNative = vec(native)
    center = (native[0] // 2, native[1] // 2)
    vCenter = vec(center)


class Color:
    alpha: RGBA = (0, 0, 0, 0)
    black:      RGB = (0, 0, 0)
    dark:       RGB = (60, 60, 60)
    gray:       RGB = (100, 100, 100)
    light:      RGB = (180, 180, 180)
    white:      RGB = (255, 255, 255)

    red:        RGB = (255, 50, 50)
    green:      RGB = (50, 255, 50)
    blue:       RGB = (50, 50, 255)
    
    cyan:       RGB = (50, 255, 255)
    magenta:    RGB = (255, 50, 255)
    yellow:     RGB = (255, 255, 50)