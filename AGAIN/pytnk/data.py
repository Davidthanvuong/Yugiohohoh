import math
import pygame as pg
from pygame import Vector2 as vec
RGB = tuple[int, int, int]
RGBA = tuple[int, int, int, int]
tff = tuple[float, float]


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

FORWARD = vec(1, 0)
UPWARD = vec(0, -1)
DEGREE90 = math.pi / 2
vZERO = vec(0, 0)
vONE = vec(1, 1)

BOTH = 2
OPPONENT = 1
PLAYER = 0

class App:
    running = True
    targetFPS = 60
    devMode = False
    gameStarted = False

    fpsTrackDur = 1.0
    native = (1400, 1000)
    devNative = (native[0] + 500, native[1])
    vNative = vec(native)
    center = (native[0] // 2, native[1] // 2)
    iv_ratio = native[1] / native[0]
    screen: pg.Surface


class Color:
    alpha = (0, 0, 0, 0)
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


# def play_sound(name):
#     pg.mixer.music.load(f"assets\\sounds\\{name}.mp3")
#     pg.mixer.music.play()

def get_sound(name):
    return pg.mixer.Sound(f"assets\\sounds\\{name}.mp3")