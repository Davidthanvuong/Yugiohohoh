import pygame as pg

from .settings import *
from enum import Enum
from importlib.util import find_spec

class RenderMode(Enum):
    LEGACY = 0
    ATLAS = 1
    OPENGL = 2
      
if not I_DONT_LIKE_OPENGL and find_spec("OpenGL"):
    RENDER = RenderMode.OPENGL
else:
    RENDER = RenderMode.LEGACY
      
    print("//////////////////////////////////////////////\n\n")
    print("It is recommended to install PyOpenGL for better performance.")
    print("vi: Khuyến khích cài PyOpenGL để tăng fps")
    print("pip install PyOpenGL PyOpenGL_accelerate")
    print("\n\n//////////////////////////////////////////////")
      
print(f"Rendering in: {RENDER.name}")

pg.init()
screen_flags = (pg.DOUBLEBUF | pg.OPENGL) if RENDER == RenderMode.OPENGL else 0
screen = pg.display.set_mode(NATIVE, screen_flags)
fonter = pg.font.Font(FONT_PATH, 20)

if RENDER == RenderMode.OPENGL:
    from .opengl_renderer import do_render, do_clear, do_write
else:
    from .legacy_renderer import do_render, do_clear, do_write

# Thằng l này phải được chạy sau khi pygame.init

def refresh_display():
    pg.display.flip()
    do_clear(screen)

def render(img, parent: vec = vec(0, 0)):
    do_render(screen, img, parent)

def write(text: str, pos: vec = vec(0, 0)):
    do_write(screen, fonter, text, pos)