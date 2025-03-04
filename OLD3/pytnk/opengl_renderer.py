from .header_pygame import *
from OpenGL.GL import * # type: ignore (Whatever, I want to import all)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .transform import Transform, Image

glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glOrtho(0, NATIVE[0], NATIVE[1], 0, -1, 1)

def create_glTexture(img: pg.Surface):
    '''Chuyển texture của Pygame sang texture của OpenGL'''
    # Thật sự là .png --> Pygame --> OpenGL. :sob:
    texture = glGenTextures(1)
    raw_size = img.get_size()
    img_data = pg.image.tobytes(img, "RGBA", True)
    # Một vài phép thuật xong gán vô ImageCache cái gl_texture
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, raw_size[0], raw_size[1], 0, 
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture

def do_clear():
    glClear(GL_COLOR_BUFFER_BIT)


def do_render(img: 'Image'):
    if not img.cache.gl_native:
        img.cache.gl_native = create_glTexture(img.cache.native)
    do_direct_render(img.cache.gl_native, img.size, img.tf, False)

def do_direct_render(sf, size: vec, tf: 'Transform', direct=True):
    if direct: 
        print("Create Texture")
        sf = create_glTexture(sf)

    pos_root = tf.pos
    uv_root = size.elementwise() * -tf.pivot
    uv_x = (uv_root[0], uv_root[0] + size.x)
    uv_y = (uv_root[1], uv_root[1] + size.y)

    glPushMatrix()
    glTranslatef(pos_root[0], pos_root[1], 0)
    
    # Bằng một lí do gì thì thứ tự của OpenGL nó ngược so với Legacy. 
    # Nên phải hậu xử lí (post_scale) trước tiền xử lí (scale) 
    # Phần rotation thì ngược chiều do bị lật lại đúng r
    glScalef(tf.scale.x, tf.scale.y, 0)
    glRotatef(tf.angle, 0, 0, 1)

    glBindTexture(GL_TEXTURE_2D, sf)
    glBegin(GL_QUADS)

    # Tạo quad gửi cho GPU
    glTexCoord2f(0, 0); glVertex2f(uv_x[0], uv_y[1])
    glTexCoord2f(1, 0); glVertex2f(uv_x[1], uv_y[1])
    glTexCoord2f(1, 1); glVertex2f(uv_x[1], uv_y[0])
    glTexCoord2f(0, 1); glVertex2f(uv_x[0], uv_y[0])
    
    glEnd()
    glPopMatrix()