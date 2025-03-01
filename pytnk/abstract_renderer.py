from enum import Enum
from .header_pygame import *
from importlib.util import find_spec
from os import environ

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .transform import Image, Text

class RenderMode(Enum):
    LEGACY = 0
    ATLAS = 1
    OPENGL = 2
      
if False and USE_OPENGL and find_spec("OpenGL"):
    RENDER = RenderMode.OPENGL
else:
    RENDER = RenderMode.LEGACY
      
print(f"Rendering in {RENDER.name}")

pg.init()
pg.display.set_caption("Yugiohohoh - Reboot 27/02/2025")
environ['SDL_VIDEO_WINDOW_POS'] = f"{(1920 - NATIVE[0]) // 2},{35}"

render_flags = (pg.DOUBLEBUF | pg.OPENGL) if RENDER == RenderMode.OPENGL else 0
screen = pg.display.set_mode(NATIVE, render_flags)

writer = pg.font.SysFont("jetbrainsmononlsemibold", FONT_SIZE)

if RENDER == RenderMode.LEGACY:
    def updateDisplay():
        pg.display.flip()
        screen.fill(colormap['dark'])
        #dummy_screen.fill((0, 0, 0, 0))

    def render(img: 'Image'):
        tf, ct = img.tf, img.cache
        grot = tf.global_rot
        px_gscale = img.size.elementwise() * tf.scale

        if img.changed or not (ct.last_grot == grot and ct.last_px_gscale == px_gscale):
            #print("Invalid, updated")
            if img.__class__.__name__ == 'Text':
                sf = writer.render(img.text, True, img.color) # type: ignore
                px_gscale = vec(sf.get_size()).elementwise() * tf.scale
            else:
                sf = ct.texture
            if px_gscale != vec(sf.get_size()): sf = pg.transform.scale(sf, px_gscale)
            if grot != 0: sf = pg.transform.rotate(sf, -grot)
            
            ct.last_grot = grot
            ct.last_px_gscale = px_gscale
            ct.topleft = px_gscale.elementwise() * (HALF - tf.pivot).rotate(grot)
            ct.cached_texture = sf
            img.changed = False
        else:
            sf = ct.cached_texture

        rect = sf.get_rect(center = tf.global_pos + ct.topleft)
        screen.blit(sf, rect)

    def write(txt: 'Text'):
        pass

elif RENDER == RenderMode.OPENGL:
    from .opengl_renderer import do_clear, do_render, do_direct_render

    def updateDisplay():
        pg.display.flip()
        #dummy_screen.fill((0, 0, 0, 0))
        do_clear()

    def render(img: 'Image'):
        do_render(img)

    def direct_render(sf: pg.Surface, size: vec, tf):
        do_direct_render(sf, size, tf)

    def write(txt: 'Text'):
        pass