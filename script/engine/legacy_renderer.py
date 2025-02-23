import pygame as pg
from .imager import Imager 
from .settings import *

def scale_by_pixel(sf: pg.Surface, size: vec, scale: vec) -> pg.Surface:
    pixel_size = (size.x * scale.x, size.y * scale.y)
    return pg.transform.scale(sf, pixel_size)

def do_clear(screen: pg.Surface):
    screen.fill((0, 0, 0))

def do_render(screen: pg.Surface, img: Imager, parent: vec):
    sf = img.shared.texture

    pos_root = img.pos + parent
    
    sf_scale = scale_by_pixel(sf, img.size, img.scale)
    sf_rot = pg.transform.rotate(sf_scale, -img.rotation)
    sf_pscale = scale_by_pixel(sf_rot, vec(sf_rot.get_size()), img.post_scale)

    uv_root = (sf_pscale.get_width() * img.scale.x * img.post_scale.x * -img.pivot.x, 
               sf_pscale.get_height() * img.scale.x * img.post_scale.x * -img.pivot.y)

    rect = sf_pscale.get_rect(topleft = pos_root + uv_root)
    screen.blit(sf_pscale, rect)

def do_write(screen: pg.Surface, fonter: pg.Font, text: str, pos: vec):
    img = fonter.render(text, True, (255, 255, 255))
    screen.blit(img, pos)