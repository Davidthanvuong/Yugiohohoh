from .settings import *
from .gameobject import *
import pygame as pg

class ImageCache:
    '''Comment here'''
    
    db: dict[int, 'ImageCache'] = {}
    
    def __init__(self, texture: pg.Surface):
        self.texture = texture
        self.gl_texture = None

    def recolor(self, a: tuple[int, int, int], b: tuple[int, int, int]):
        self.gl_texture = None
        for x in range(self.texture.get_width()):
            for y in range(self.texture.get_height()):
                if self.texture.get_at((x, y)) == a:
                    self.texture.set_at((x, y), b)

    @staticmethod
    def load_cache(path: str) -> 'ImageCache':
        '''Cố gắng Load texture và OpenGL texture từ bộ nhớ'''
        poly = hash(path)
        if poly not in ImageCache.db:
            img = pg.image.load(f"image\\{path}").convert_alpha()
            ImageCache.db[poly] = ImageCache(img)

        return ImageCache.db[poly]


class Imager(GameObject):
    '''Wrapper cho thằng pygame.Surface\n
    Thêm tính năng lưu hash, cân mọi pivot, tối ưu cho OpenGL'''

    def __init__(self, path: str = "", size = vec(0, 0), sf: Optional[pg.Surface] = None, **kwargs):
        super().__init__(**kwargs)
        self.shared = ImageCache(sf) if sf != None else ImageCache.load_cache(path)

        # Mặc định sang kích thước của ảnh
        if size != vec(0, 0):
            self.size = size
        else:
            sz = self.shared.texture.get_size()
            self.size = vec(sz[0], sz[1])