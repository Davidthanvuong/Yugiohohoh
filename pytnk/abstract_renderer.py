from enum import Enum
from .header_pygame import *
from importlib.util import find_spec

class RenderMode(Enum):
    LEGACY = 0
    ATLAS = 1
    OPENGL = 2
      
if USE_OPENGL and find_spec("OpenGL"):
    RENDER = RenderMode.OPENGL
else:
    RENDER = RenderMode.LEGACY
      
print(f"Rendering in {RENDER.name}")

pg.init()
pg.display.set_caption("Yugiohohoh - Reboot 27/02/2025")

render_flags = 0#(pg.DOUBLEBUF | pg.OPENGL) if RENDER == RenderMode.OPENGL else 0
screen = pg.display.set_mode(NATIVE, render_flags)
writer = pg.font.Font("Comic.ttf", 20)