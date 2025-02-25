from importer.pygame import *
from engine.imagecache import ImageCache

class Transform():
    '''Hỗ trợ trong việc xử lí vị trí, tính chất của ảnh và các vật con (childrens)'''
    pivots: dict[str, 'Transform'] = {}
    
    def __init__(self, pos = vec(0, 0), scale = vec(ONE), post_scale = vec(ONE), 
                 spin = 0.0, pivot = vec(HALF), parent: No['Transform'] = None,
                 imgpath: str = "", imgsize = vec(ZERO), **kwargs):
        self.pos = pos
        self.scale = scale
        self.post_scale = post_scale
        self.spin = spin
        self.pivot = pivot
        self.parent = parent

        if imgpath == "": # Không dùng ảnh thì để ảnh rỗng :penguin:
              self.shared = ImageCache() 
        else: self.shared = ImageCache.fetch(imgpath)
        
        if imgsize != vec(ZERO): # Mặc định sang kích thước của ảnh
              self.imgsize = imgsize
        else: self.imgsize = vec(self.shared.texture.get_size())

        super().__init__(**kwargs)

    @staticmethod
    def setupPivot():
        '''Khởi tạo 9 góc tọa độ trong màn hình để hỗ trợ scaling'''
        names = [
            'topleft', 'midtop', 'topright',
            'midleft', 'center', 'midright',
            'bottomleft', 'midbottom', 'bottomright'
        ]
        for i in range(0, 3):
            for j in range(0, 3):
                pivot = vec(0.5 * i, 0.5 * j)
                pos = vec(NATIVE[0] * pivot[0], NATIVE[1] * pivot[1])
                Transform.pivots[names[i*3 + j]] = Transform(pos=pos, pivot=pivot)

    @abstractmethod
    def update(self): pass

    @abstractmethod
    def on_debugging(self): pass