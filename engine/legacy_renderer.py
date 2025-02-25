from importer.pygame import *
from .transform import Transform 

def scale_by_pixel(sf: pg.Surface, size: vec, scale: vec) -> pg.Surface:
    pixel_size = (size.x * scale.x, size.y * scale.y)
    return pg.transform.scale(sf, pixel_size)

def do_clear(screen: pg.Surface):
    screen.fill((0, 0, 0))

def do_displayChange(x, y):
    pass

def do_render(screen: pg.Surface, img: Transform):
    sf = img.shared.texture

    pos_root = img.pos
    
    _sf = scale_by_pixel(sf, img.imgsize, img.scale)
    if img.spin != 0:               _sf = pg.transform.rotate(_sf, -img.spin)
    if img.post_scale != vec(ONE): _sf = scale_by_pixel(_sf, vec(_sf.get_size()), img.post_scale)

    uv_root = (_sf.get_width() * img.scale.x * img.post_scale.x * -img.pivot.x, 
               _sf.get_height() * img.scale.x * img.post_scale.x * -img.pivot.y)

    rect = _sf.get_rect(topleft = pos_root + uv_root)
    screen.blit(_sf, rect)

# def do_write(screen: pg.Surface, fonter: pg.font.Font, text: str, pos: vec):
#     img = fonter.render(text, True, (255, 255, 255))
#     screen.blit(img, pos)