from .header_pygame import *

class ImageCache:
    '''Load & lưu Texture động (dynamically) vào bộ nhớ, khi nào cần lấy ra'''
    database: dict[int, 'ImageCache'] = {}
    
    def __init__(self, path: str = "", bh = False):
        if path == "":
            self.texture = pg.Surface((0, 0), pg.SRCALPHA)
        else:
            self.texture = pg.image.load(f"assets\\images\\{path}").convert_alpha()
        self.gl_texture = None

        self.bullethell = bh
        self.cached_texture = self.texture
        self.last_grot = 0.0
        self.last_px_gscale = vec(ZERO)
        self.topleft = vec(ZERO)

    @staticmethod
    def fetch(path: str, bh = False) -> 'ImageCache':
        '''Cố gắng Load texture và OpenGL texture từ bộ nhớ, không có thì tạo cái mới'''        
        poly = hash(path)
        if poly not in ImageCache.database:
            ImageCache.database[poly] = ImageCache(path)

        return ImageCache.database[poly]    



class Image(Component):
    '''Ảnh được cập nhật lười. Bật bullethell=True nếu là projectile và có rất nhiều biến thể xoay (ăn RAM 64x64)'''

    def __init__(self, path: str = "", size: tff = ZERO, bullethell = False, standalone = False, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.bullethell = bullethell
        self.standalone = standalone
        # Nếu là standalone thì không lưu vô database hay share
        self.cache = ImageCache(path, bh=bullethell) if standalone else ImageCache.fetch(path, bullethell)
        self.size = vec(size if size != ZERO else self.cache.texture.get_size())
        self.changed = True


    def __getstate__(self):
        '''Lưu vật đến pickle'''
        state = self.__dict__.copy()
        state.pop("cache", None)
        #super().__getstate__() # loại hoặc parse lại các runtime có lỗi ở inheritance
        return state
    
    def __setstate__(self, state):
        '''Đọc vật từ pickle'''
        self.__dict__.update(state)
        self.changed = True

        if self.standalone:
            self.cache = ImageCache(self.path, bh=self.bullethell)
        else:
            self.cache = ImageCache.fetch(self.path, self.bullethell)

    def update_render(self):
        render(self)



class Text(Image):
    '''Ghi chữ có tiện ích ở đây'''
    def __init__(self, text: str = "", color = colormap['white'], **kwargs):
        super().__init__(standalone=True, **kwargs)
        self.text = text
        self.color = color

    def update_render(self):
        render(self)