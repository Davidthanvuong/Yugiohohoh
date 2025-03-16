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
    def __init__(self, overrideHitbox = False, support_overlay = False, support_flip = False, notLazy = False):
        self.overrideHitbox = overrideHitbox
        self.notLazy = notLazy
        self.support_flip = support_flip
        self.support_overlay = support_overlay

        self.overlay_opacity = 0
        self.overlay_color: RGB = Color.white

        self.c_surface = pg.Surface((0, 0))
        self.c_rot = 69420.69420
        self.c_scale = vec(ZERO)
        self.c_pixels = vec(ZERO)
        self.c_topleft = vec(ZERO)

    def try_flipping(self, sf: pg.Surface):
        if self.c_scale.x < 0 and self.c_scale.y < 0:
            sf = pg.transform.flip(sf, True, True)
            self.c_pixels.x = abs(self.c_pixels.x)
            self.c_pixels.y = abs(self.c_pixels.y)

        elif self.c_scale.x < 0: 
            sf = pg.transform.flip(sf, True, False)
            self.c_pixels.x = abs(self.c_pixels.x)

        elif self.c_scale.y < 0:
            sf = pg.transform.flip(sf, False, True)
            self.c_pixels.y = abs(self.c_pixels.y)
            
        return sf
    
    def render_lazy(self, f_getSf: Callable[[], tuple[pg.Surface, vec]], force_update = False):
        lazyImg = not force_update and not self.notLazy
        lazyImg = lazyImg and (self.c_rot == self.transf.g_rot) and (self.c_scale == self.transf.g_scale)

        if not lazyImg:
            # Chỉ update lại ảnh (local) khi thay đổi kích thước hoặc góc xoay
            sf, imgsize = f_getSf()
            self.c_rot = self.transf.g_rot
            self.c_scale = self.transf.g_scale.copy()
            self.c_pixels = self.c_scale.elementwise() * imgsize
            if self.support_flip:
                sf = self.try_flipping(sf)

            sf = pg.transform.scale(sf, self.c_pixels)
            
            rotatable = not self.transf.straight and not (-0.5 <= self.c_rot <= 0.5)
            if rotatable: sf = pg.transform.rotate(sf, self.c_rot)

            offset = (CENTER - self.transf.anchor)
            self.c_surface = sf
            if self.support_overlay:
                ov = self.c_overlay = sf.copy()
                ov.fill(self.overlay_color, special_flags=pg.BLEND_ADD)
            self.c_topleft = (self.c_pixels.elementwise() * offset).rotate(-self.c_rot)

            if self.overrideHitbox:
                self.transf.l_hitboxSize = self.c_pixels

        rect = self.c_surface.get_rect(center = self.transf.g_pos + self.c_topleft)
        App.screen.blit(self.c_surface, rect)

        if self.support_overlay and self.overlay_opacity != 0:
            self.c_overlay.set_alpha(self.overlay_opacity)
            App.screen.blit(self.c_overlay, rect)
        


class Image(Renderer):
    '''Ảnh được cập nhật lười'''

    def __init__(self, path: str = "", size: tff = ZERO, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.shared = SharedImg.getImage(path, size)
        self.imgsize = vec(size if size != ZERO else self.shared.native.get_size())

    def switchImage(self, path: str, size: No[tff] = None):
        self.path = path
        self.shared = SharedImg.getImage(path, size if size else (self.imgsize.x, self.imgsize.y))

    def getDefaultSf(self):
        sf = self.shared.native
        return sf, self.imgsize

    def update_render(self):
        self.render_lazy(self.getDefaultSf)



class Text(Renderer):
    '''Tiện ích viết chữ'''

    def __init__(self, text: str = "", color = Color.white, path = "jb_semibold", size = 14, **kwargs):
        super().__init__(**kwargs)
        self.font = SharedImg.getFont(path, size)
        self.fontdir = path, size
        self.text = text
        self.old_hash = hash(text)
        self.color = color

    def getNew_textRender(self):
        sf = self.font.render(self.text, False, self.color)
        return sf, vec(sf.get_size())

    def update_render(self):
        if hash(self.text) != self.old_hash:
            force = True
            self.old_hash = hash(self.text)
        else: force = False
        self.render_lazy(self.getNew_textRender, force)