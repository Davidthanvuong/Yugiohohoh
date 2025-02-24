import pygame as pg
from .imager import *
from .settings import *
from OpenGL.GL import * # type: ignore (Whatever, I want to import all)

glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glOrtho(0, NATIVE[0], NATIVE[1], 0, -1, 1)

def create_glTexture(img: Imager):
    texture = glGenTextures(1)
    raw_size = img.shared.texture.get_size()
    img_data = pg.image.tobytes(img.shared.texture, "RGBA", True)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, raw_size[0], raw_size[1], 0, 
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    img.shared.gl_texture = texture
    return texture

def do_clear(_):
    glClear(GL_COLOR_BUFFER_BIT)

def do_render(_, img, parent: vec):
    
    # Chưa generate thì mới tạo
    if img.shared.gl_texture is None: 
        create_glTexture(img)
    texture = img.shared.gl_texture

    # wpos: vị trí trên màn hình
    # uv 0-1: tham số các đỉnh
    pos_root = img.pos + parent
    uv_root = (img.size.x * -img.pivot.x, img.size.y * -img.pivot.y)
    uv_x = (uv_root[0], uv_root[0] + img.size.x)
    uv_y = (uv_root[1], uv_root[1] + img.size.y)

    glPushMatrix()
    glTranslatef(pos_root[0], pos_root[1], 0)
    # Bằng một lí do gì thì thứ tự của OpenGL nó ngược so với Legacy. 
    # Nên phải hậu xử lí (post_scale) trước tiền xử lí (scale) 
    # Phần rotation thì ngược chiều do bị lật lại đúng r
    glScalef(img.post_scale.x, img.post_scale.y, 0)
    glRotatef(img.rotation, 0, 0, 1)
    glScalef(img.scale.x, img.scale.y, 0)

    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)

    # Tạo quad gửi cho GPU
    glTexCoord2f(0, 0); glVertex2f(uv_x[0], uv_y[1])
    glTexCoord2f(1, 0); glVertex2f(uv_x[1], uv_y[1])
    glTexCoord2f(1, 1); glVertex2f(uv_x[1], uv_y[0])
    glTexCoord2f(0, 1); glVertex2f(uv_x[0], uv_y[0])
    
    glEnd()
    glPopMatrix()

def do_write(_, _2, text: str, pos: vec):
    print(text)