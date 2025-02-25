from importer.pygame import *
from engine.imagecache import ImageCache
import math

class Transform():
    '''Hỗ trợ trong việc xử lí vị trí, tính chất của ảnh và các vật con (childrens)'''
    
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

    # @staticmethod
    # def setupPivot():
    #     global pivots
    #     '''Khởi tạo 9 góc tọa độ trong màn hình để hỗ trợ scaling'''
    #     names = [
    #         'topleft', 'midtop', 'topright',
    #         'midleft', 'center', 'midright',
    #         'bottomleft', 'midbottom', 'bottomright'
    #     ]
    #     for i in range(0, 3):
    #         for j in range(0, 3):
    #             pivot = vec(0.5 * i, 0.5 * j)
    #             pos = vec(NATIVE[0] * pivot[0], NATIVE[1] * pivot[1])
    #             pivots[names[i*3 + j]] = Transform(pos=pos, pivot=pivot)

    def global_spin(self) -> float:
        '''Tham số toàn cầu (readonly) của góc xoay vật'''
        spin = self.spin
        if self.parent: spin += self.parent.global_spin()
        return spin
    
    def global_scale(self) -> vec:
        '''Tham số toàn cầu (readonly) của kích thước vật'''
        scale = self.post_scale
        if self.parent: 
            gs = self.global_scale() 
            scale.x *= gs.x
            scale.y *= gs.y
        return scale
    
    def global_pos(self) -> vec:
        '''Tham số toàn cầu (readonly) của vị trí vật'''
        pos = self.pos
        if self.parent:
            parent_pos = self.parent.global_pos()
            parent_scale = self.parent.global_scale()
            #parent_rot = math.radians(self.parent.global_spin())

            # Scale vị trí dựa trên kích thước và góc xoay của vật chủ
            local_offset = vec( self.pos.x * parent_scale.x,
                                self.pos.y * parent_scale.y)
            
            rotated_offset = local_offset.rotate(self.parent.global_spin())

            return parent_pos + rotated_offset
        return pos
    
    @abstractmethod
    def update(self): pass

    @abstractmethod
    def on_debugging(self): pass

#pivots: dict[str, 'Transform'] = {}