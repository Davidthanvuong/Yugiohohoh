from importer.pygame import *
from typing import Union

tempTexture = pg.Surface((0, 0))

class ImageCache:
    '''Load & lưu Texture động (dynamically) vào bộ nhớ, khi nào cần lấy ra'''
    db: dict[int, 'ImageCache'] = {}
    
    def __init__(self, path: Union[str, pg.Surface, None] = None):#path: str = "", texture: pg.Surface = tempTexture):
        if isinstance(path, pg.Surface):
            self.texture = path
        elif isinstance(path, str):
            self.texture = pg.image.load(f"images\\{path}").convert_alpha()
        else:
            self.texture = tempTexture
        self.gl_texture = None

    @staticmethod
    def fetch(path: str) -> 'ImageCache':
        '''Cố gắng Load texture và OpenGL texture từ bộ nhớ, không có thì tạo cái mới'''
        poly = hash(path)
        if poly not in ImageCache.db:
            ImageCache.db[poly] = ImageCache(path)

        return ImageCache.db[poly]
    
    # todo: Move to image manipulator?
    def replace_color(self, a: tuple[int, int, int], b: tuple[int, int, int]):
        self.gl_texture = None
        for x in range(self.texture.get_width()):
            for y in range(self.texture.get_height()):
                if self.texture.get_at((x, y)) == a:
                    self.texture.set_at((x, y), b)
