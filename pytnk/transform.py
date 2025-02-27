from .header_objects import *
from typing import TypeVar, Union, cast
from dataclasses import dataclass

T = TypeVar("T", bound="Interface")

@dataclass
class MouseInfo:
    pos: vec
    clicked: bool
    host: No['Interface']

mouse = MouseInfo(vec(1, 0), False, None)


def update_mouse():
    '''Cập nhật chuột duy nhất, lưu lại host cũ khi còn tồn tại hay đang đè'''
    global mouse

    host = mouse.host if mouse.host else None # Lỡ bay màu thì hủy
    mouse.pos = vec(pg.mouse.get_pos())
    mouse.clicked = pg.mouse.get_pressed()[0]
    mouse.host = host



class Translite:
    '''Phiên bản nhẹ kí của Transform'''

    # Info của chuột, xóa khi gặp 1 vật tương tác đc

    def __init__(self, pos: tff = CENTER, rot: float = 0, scale: tff = ONE, pivot: tff = HALF, 
                 hitbox: tff = (64, 64), parent: No['Translite'] = None):
        print(pos, scale)
        self.pos = vec(pos)
        self.rot = rot
        self.scale = vec(scale)
        self.pivot = vec(pivot)
        self.parent = parent
        self.hitbox = vec(hitbox)
        self.coms: dict[type['Interface'], 'Interface'] = {}

    def get(self, com: type[T]) -> T:
        return cast(T, self.coms[com])

    def click_update(self):
        for com in self.coms.values():
            com.click_update()

    def render_update(self):
        for com in self.coms.values():
            com.render_update()


class Interface:
    '''Class để chạy các chức năng từ vật (Translite)'''

    def __init__(self, tf: Translite):
        self.tf = tf
        tf.coms[self.__class__.mro()[0]] = self
        #for base in reversed(self.__class__.mro())

    @abstractmethod
    def click_update(self): pass

    @abstractmethod
    def render_update(self): pass


class IClickable(Interface):
    '''Click'''
    def __init__(self, clickable=True, draggable=False, **kwargs):
        super().__init__(**kwargs)

        self.clickable = clickable
        self.draggable = draggable # Cho phép kéo thả
        self.hovering = False
        self.clicking = False

    def try_getMouse(self):
        '''Thử lấy chuột trong hitbox'''
        if mouse.host and mouse.host is not self:
            return False
    
        box = self.tf.hitbox.elementwise() * self.tf.scale
        a = box.elementwise() * -self.tf.pivot
        b = a + box
        rel = (mouse.pos - self.tf.pos).rotate(-self.tf.rot)

        return (a.x <= rel.x <= b.x) and \
               (a.y <= rel.y <= b.y)

    def click_update(self):
        if self.try_getMouse():
            if not self.hovering:
                mouse.host = self # Đánh dấu vật đã dùng chuột
                self.on_startHover()
                self.hovering = True
            
            if not self.clickable:
                return
            if mouse.clicked:
                if not self.clicking:
                    self.on_startClick()
                    self.clicking = True
                self.on_clicking()
            elif self.clicking:
                self.on_stopClick()
                self.clicking = False

            self.on_hovering()
        elif self.hovering:
            self.on_stopHover()
            mouse.host = None
            self.hovering = False

    # Bắt buộc inheritance phải có
    @abstractmethod
    def render_update(self): pass

    # Hàm rỗng nhưng không abstract để cho inheritance
    def on_startHover(self): pass
    def on_startClick(self): pass
    def on_stopHover(self): pass
    def on_stopClick(self): pass
    def on_hovering(self): pass
    def on_clicking(self): pass



tempTexture = pg.Surface((0, 0))

class ImageCache:
    '''Load & lưu Texture động (dynamically) vào bộ nhớ, khi nào cần lấy ra'''
    db: dict[int, 'ImageCache'] = {}
    
    def __init__(self, path: Union[str, pg.Surface, None] = None):#path: str = "", texture: pg.Surface = tempTexture):
        if isinstance(path, pg.Surface):
            self.texture = path
        elif isinstance(path, str):
            self.texture = pg.image.load(f"assets\\images\\{path}").convert_alpha()
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


class Image(Interface):
    '''Ảnh'''

    def __init__(self, imgpath: str, imgsize: No[tff] = None, **kwargs):
        super().__init__(**kwargs)
        self.shared = ImageCache.fetch(imgpath)
        self.imgsize = vec(imgsize if imgsize else self.shared.texture.get_size())

    def click_update(self):
        pass

    def render_update(self):
        self.direct_render(self.shared.texture, self.imgsize, self.tf.pivot)

    def direct_render(self, texture: pg.Surface, size: vec, pivot: vec, offset = vec(ZERO)):
        img = pg.transform.scale(texture, size.elementwise() * self.tf.scale)
        if self.tf.rot != 0: img = pg.transform.rotate(img, -self.tf.rot)

        topleft = (size + offset).elementwise() * (self.tf.scale.elementwise() * (HALF - pivot))
        rect = img.get_rect(center = self.tf.pos + topleft.rotate(self.tf.rot))
        screen.blit(img, rect)