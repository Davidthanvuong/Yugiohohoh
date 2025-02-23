from .settings import *
import pygame as pg

class ImageCache:
    def __init__(self, texture: pg.Surface):
        self.texture = texture
        self.gl_texture = None

    def recolor(self, a: tuple[int, int, int], b: tuple[int, int, int]):
        self.gl_texture = None
        for x in range(self.texture.get_width()):
            for y in range(self.texture.get_height()):
                if self.texture.get_at((x, y)) == a:
                    self.texture.set_at((x, y), b)

db: dict[int, ImageCache] = {}

def load_cache(path: str) -> ImageCache:
    '''Cố gắng Load texture và OpenGL texture từ bộ nhớ'''
    poly = hash(path)
    if poly not in db:
        img = pg.image.load(f"image\\{path}").convert_alpha()
        db[poly] = ImageCache(img)

    return db[poly]


class Imager:
    '''Wrapper cho thằng pygame.Surface\n
    Thêm tính năng lưu hash, cân mọi pivot, tối ưu cho OpenGL'''

    def __init__(self, path: str, pos: vec = vec(0, 0), size: vec = vec(0, 0), 
                    scale: vec = vec(1, 1), post_scale: vec = vec(1, 1), rotation: float = 0.0, pivot: vec = vec(0.5, 0.5)):
        self.shared = load_cache(path)
        self.pos = pos
        self.post_scale = post_scale
        self.scale = scale
        self.rotation = rotation
        self.pivot = pivot

        if size != vec(0, 0):
            self.size = size
        else:
            sz = self.shared.texture.get_size()
            self.size = vec(sz[0], sz[1])