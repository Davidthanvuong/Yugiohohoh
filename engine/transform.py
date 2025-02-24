from importer.pygame import *
from engine.imagecache import ImageCache

class Transform():
    '''Hỗ trợ trong việc xử lí vị trí, tính chất của vật'''
    def __init__(self, pos = vec(0, 0), scale = vec(ONE), post_scale = vec(ONE), 
                 spin = 0.0, pivot = vec(HALF), parent: No['Transform'] = None, **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.scale = scale
        self.post_scale = post_scale
        self.spin = spin
        self.pivot = pivot
        self.parent = parent

    @abstractmethod
    def update(self): pass

    @abstractmethod
    def on_debugging(self): pass


class Imager(Transform):
    '''Wrapper cho thằng pygame.Surface'''

    def __init__(self, path: str = "", size = vec(ZERO), **kwargs):
        super().__init__(**kwargs)
        if path == "": # Ảnh rỗng
              self.shared = ImageCache() 
        else: self.shared = ImageCache.fetch(path)
        
        if size != vec(ZERO): # Mặc định sang kích thước của ảnh
              self.size = size
        else: self.size = vec(self.shared.texture.get_size())