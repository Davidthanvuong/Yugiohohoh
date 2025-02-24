from importer.pygame import *

tempTexture = pg.Surface((0, 0))

class ImageCache:
    '''Load & lưu Texture động (dynamically) vào bộ nhớ, khi nào cần lấy ra'''
    db: dict[int, 'ImageCache'] = {}
    
    def __init__(self, texture: pg.Surface = tempTexture):
        self.texture = texture
        self.gl_texture = None

    @staticmethod
    def fetch(path: str) -> 'ImageCache':
        '''Cố gắng Load texture và OpenGL texture từ bộ nhớ'''
        poly = hash(path)
        if poly not in ImageCache.db:
            img = pg.image.load(f"images\\{path}").convert_alpha()
            ImageCache.db[poly] = ImageCache(img)

        return ImageCache.db[poly]
    
    # todo: Move to image manipulator?
    def replace_color(self, a: tuple[int, int, int], b: tuple[int, int, int]):
        self.gl_texture = None
        for x in range(self.texture.get_width()):
            for y in range(self.texture.get_height()):
                if self.texture.get_at((x, y)) == a:
                    self.texture.set_at((x, y), b)
