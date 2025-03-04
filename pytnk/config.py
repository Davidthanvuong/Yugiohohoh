import pygame as pg
from pygame import Vector2 as vec
from pygame.event import peek as pgpeek
from dataclasses import dataclass
from typing import Optional as No
from typing import Final

@dataclass
class MouseInfo:
    pos: vec
    clicked: bool
    host: No[object]
    lastFocus: No[object]

mouse = MouseInfo(vec(1, 0), False, None, None)

class Window:
    running = True
    targetFPS = 60
    fontScale = 1
    useOpenGL = False
    native = (1900, 1000)
    middle = (native[0]//2, native[1]//2)
    devMode = False

colormap: Final[dict[str, tuple[int, int, int]]] = {
    'dark': (60, 60, 60),
    'gray': (100, 100, 100),
    'light': (180, 180, 180),
    'white': (255, 255, 255),
    'forward': (255, 50, 50),
    'upward': (50, 50, 255),
    'freedom': (50, 255, 50),
    'relation': (50, 150, 150),
    'pivot': (0, 255, 0),
}