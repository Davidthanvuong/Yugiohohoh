from .engine import *

class SharedImg:
    img_db: dict[str, 'SharedImg'] = { }
    font_db: dict[tuple[str, int], Font] = {}

    '''Load & lưu Texture động (dynamically) vào bộ nhớ, khi nào cần lấy ra'''
    def __init__(self, path: str, expected: tff = ZERO, small: tff = ZERO):
        self.native = pg.image.load(f"assets\\images\\{path}").convert_alpha()
        if expected != ZERO:
            self.native = pg.transform.scale(self.native, expected)

        self.whiteImg = None

    # def fillColor(self, color: RGB):
        img = self.native
        
           
    def getWhiteImage(self):
        if not self.whiteImg:
            img = self.whiteImg = self.native.copy()
            for y in range(img.get_height()):
                for x in range(img.get_width()):
                    imgcolor = img.get_at((x, y))
                    if imgcolor.a > 0:
                        img.set_at((x, y), Color.white)

        return self.whiteImg

    @classmethod
    def getImage(cls, path: str, size: tff = ZERO):
        sh = cls.img_db.get(path)
        if not sh: 
            sh = cls.img_db[path] = cls(path, size)
        return sh
    
    @classmethod
    def getFont(cls, path: str, size: int):
        ff = cls.font_db.get((path, size))
        if not ff:
            ff = cls.font_db[(path, size)] = pg.font.Font(f"assets\\{path}.ttf", size)
        return ff
    

class Renderer(Component):
    def __init__(self, overrideHitbox = False, notLazy = False):
        self.overrideHitbox = overrideHitbox
        self.notLazy = notLazy

        self.c_surface = pg.Surface((0, 0))
        self.c_rot = 69420.69420
        self.c_scale = vec(ZERO)
        self.c_pixels = vec(ZERO)
        self.c_topleft = vec(ZERO)

    def render_lazy(self, f_getSf: Callable[[], tuple[pg.Surface, vec]], force_update = False):
        lazyImg = not force_update and not self.notLazy
        lazyImg = lazyImg and (self.c_rot == self.transf.g_rot) and (self.c_scale == self.transf.g_scale)

        if not lazyImg:
            # Chỉ update lại ảnh (local) khi thay đổi kích thước hoặc góc xoay
            oldSf, imgsize = f_getSf()
            self.c_rot = self.transf.g_rot
            self.c_scale = self.transf.g_scale.copy()
            self.c_pixels = self.c_scale.elementwise() * imgsize
            rotatable = not self.transf.straight and not (-1.0 <= self.c_rot <= 1.0)

            sf = pg.transform.scale(oldSf, self.c_pixels)
            if rotatable: sf = pg.transform.rotate(sf, self.transf.g_rot)

            self.c_surface = sf
            offset = (CENTER - self.transf.anchor)
            self.c_topleft = (self.c_pixels.elementwise() * offset).rotate(-self.c_rot)
            if self.overrideHitbox:
                self.transf.l_hitboxSize = self.c_pixels
                #self.transf.l_hitboxTopleft = self.c_topleft

        rect = self.c_surface.get_rect(center = self.transf.g_pos + self.c_topleft)
        App.display.blit(self.c_surface, rect)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.pop("c_surface", None)
        return state
    
    def __setstate__(self, state):
        super().__setstate__(state)
        self.c_lazy = False
        self.c_surface = pg.Surface((0, 0))



class Image(Renderer):
    '''Ảnh được cập nhật lười'''

    def __init__(self, path: str = "", size: tff = ZERO, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.shared = SharedImg.getImage(path, size)
        self.imgsize = vec(size if size != ZERO else self.shared.native.get_size())
        self.flashing = False
        self.c_flash = False

    def switchImage(self, path: str, size: No[tff] = None):
        self.path = path
        self.shared = SharedImg.getImage(path, size if size else (self.imgsize.x, self.imgsize.y))

    def getDefaultSf(self):
        sf = self.shared.getWhiteImage() if self.flashing else self.shared.native
        return sf, self.imgsize

    def update_render(self):
        self.render_lazy(self.getDefaultSf, self.flashing != self.c_flash)
        self.c_flash = self.flashing
    
    def __getstate__(self):
        state = super().__getstate__()
        state.pop("shared", None)
        return state
    
    def __setstate__(self, state):
        super().__setstate__(state)
        self.c_updated = False
        self.shared = SharedImg.getImage(self.path)



class Text(Renderer):
    '''Tiện ích viết chữ'''

    def __init__(self, text: str = "", color = Color.white, path = "jb_semibold", size = 14, **kwargs):
        super().__init__(**kwargs)
        self.font = SharedImg.getFont(path, size)
        self.fontdir = path, size
        self.text = text
        self.old_hash = hash(text)
        self.color = color

    def __getstate__(self):
        state = super().__getstate__()
        state.pop("font", None)
        return state
    
    def __setstate__(self, state):
        super().__setstate__(state)
        self.font = SharedImg.getFont(self.fontdir[0], self.fontdir[1])

    def getNew_textRender(self):
        sf = self.font.render(self.text, False, self.color)
        return sf, vec(sf.get_size())

    def update_render(self):
        if hash(self.text) != self.old_hash:
            force = True
            self.old_hash = hash(self.text)
        else: force = False
        self.render_lazy(self.getNew_textRender, force)

# class Text(Renderer):
#     '''Ghi chữ có tiện ích ở đây'''

#     def __init__(self, text: str = "", color = Color.white, path = "jb_semibold", size = 14, **kwargs):
#         super().__init__(**kwargs)
#         #self.fontsize = preset
#         self.font = SharedImg.getFont(path, size)
#         self.fontsize = size
#         self.text = text
#         self.old_hash = hash(text)
#         self.color = color

#         self.cache_id = 0
#         self.cached_text = pg.Surface((0, 0))
#         self.last_grot = 0.0
#         self.last_gscale = vec(ZERO)
#         self.pixels = vec(ZERO)
#         self.topleft = vec(ZERO)
    
#     def __getstate__(self):
#         state = self.__dict__.copy()
#         state.pop("cached_text", None)
#         return state
    
#     def __setstate__(self, state):
#         self.__dict__.update(state)
#         self.cache_id = 0

#     def update_render(self):
#         if hash(self.text) != self.old_hash:
#             self.changed = True
#             self.old_hash = hash(self.text)