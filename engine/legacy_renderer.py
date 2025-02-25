from importer.pygame import *
from .transform import Transform 

def scale_by_pixel(sf: pg.Surface, size: vec, scale: vec) -> pg.Surface:
    pixel_size = (size.x * scale.x, size.y * scale.y)
    return pg.transform.scale(sf, pixel_size)

def do_clear(screen: pg.Surface):
    screen.fill((0, 0, 0))

def do_render(screen: pg.Surface, tf: Transform):
    sf = tf.shared.texture

    pos_root = tf.global_pos()
    
    _sf = scale_by_pixel(sf, tf.imgsize, tf.scale)
    if tf.spin != 0.0:            _sf = pg.transform.rotate(_sf, -tf.spin)
    if tf.post_scale != vec(ONE): _sf = scale_by_pixel(_sf, vec(_sf.get_size()), tf.post_scale)

    uv_root = (_sf.get_width() * tf.scale.x * tf.post_scale.x * -tf.pivot.x, 
               _sf.get_height() * tf.scale.x * tf.post_scale.x * -tf.pivot.y)

    #pg.draw.circle(screen, (255, 0, 0), pos_root, 5)
    pg.draw.circle(screen, (255, 0, 255), uv_root, 6)
    rect = _sf.get_rect(topleft = pos_root + uv_root)
    screen.blit(_sf, rect)

# def do_write(screen: pg.Surface, fonter: pg.font.Font, text: str, pos: vec):
#     img = fonter.render(text, True, (255, 255, 255))
#     screen.blit(img, pos)