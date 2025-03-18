from .engine import *
from pygame import transform as Img


class LazySurface:
    def __init__(self, transf: Transform, enable_overlay = False):
        self.transf = transf
        self.enable_overlay = enable_overlay

        self.c_surface = pg.Surface((0, 0))
        self.c_pos = vZERO
        self.c_rot = 69420.69420
        self.c_scale = vZERO
        self.c_pixels = vZERO
        self.c_topleft = vZERO

    @property
    def unchanged(self):
        return (self.c_rot == self.transf.g_rot) and (self.c_scale == self.transf.g_scale)

    def recreate(self, img: pg.Surface, imgsize: vec, overlay_color: RGB = Color.white):
        tf = self.transf
        rotatable = tf.enable_rotation and not (-0.5 <= self.transf.g_rot <= 0.5)
        px = tf.g_scale.elementwise() * imgsize

        if px.x < 0 or px.y < 0:
            img = Img.flip(img, px.x < 0, px.y < 0)
            px.x, px.y = abs(px.x), abs(px.y)

        if img.get_size() != (px.x, px.y): img = Img.scale(img, px)
        if rotatable: img = Img.rotate(img, tf.g_rot)

        if self.enable_overlay:
            overlay = self.c_overlay = img.copy()
            overlay.fill(overlay_color, special_flags=pg.BLEND_ADD)

        # if App.debugMode:
        #     print("E")
        #     debugText = pg.font.Font(None, 32).render(f"{rotatable}: {self.transf.rot}", True, Color.green)
        #     img.blit(debugText, (0, 0))

        self.c_surface = img
        self.c_rot = tf.g_rot
        self.c_scale = tf.g_scale.copy()
        self.c_pixels = px
        self.c_topleft = (px.elementwise() * (CENTER - tf.anchor)).rotate(-self.c_rot)

    def render(self, alpha = 255, overlay_alpha = 0, canvas: No[pg.Surface] = None, newPos: No[vec] = None):
        if not canvas: canvas = App.screen
        pos = newPos if newPos else self.transf.g_pos
        rect = self.c_surface.get_rect(center = pos + self.c_topleft)
        self.c_surface.set_alpha(alpha)
        canvas.blit(self.c_surface, rect)
        
        if self.enable_overlay and overlay_alpha != 0:
            self.c_overlay.set_alpha(overlay_alpha)
            canvas.blit(self.c_overlay, rect)



class LoadedImage:
    database: dict[str, 'LoadedImage'] = {}

    def __init__(self, path: str, expectedSize: No[tff] = None):
        img = pg.image.load(f"assets/images/{path}").convert_alpha()
        if not expectedSize:
            self.size = vec(img.get_size())
            self.native = img
            return

        img = Img.scale(img, expectedSize)
        self.size = vec(expectedSize)
        self.native = img

    @classmethod
    def load(cls, path: str, size: No[tff] = None):
        '''Load ảnh từ bộ nhớ nếu có. Lưu theo native & các tỉ lệ LoD'''
        image = cls.database.get(path)
        if not image:
            image = cls.database[path] = cls(path, size)
        return image



class Image(Component):
    def __init__(self, path: str = "", size: No[tff | int] = None, enable_overlay = False, override_hitbox = False):
        self.path = path
        self.image = LoadedImage.load(path)
        self.size = vec(size) if size else vec(self.image.size)
        self.enable_overlay = enable_overlay
        self.override_hitbox = override_hitbox
        self.overlay_alpha = 0
        self.overlay_color = Color.white
        self.alpha = 255
    
    def after_init(self):
        self.lazy = LazySurface(self.transf, self.enable_overlay)

    def switchImage(self, path: str):
        self.path = path
        self.image = LoadedImage.load(path)

    def update_render(self):
        if not self.lazy.unchanged:
            self.lazy.recreate(self.image.native, self.size, self.overlay_color)
            if self.override_hitbox: self.transf.hitbox = self.size

        self.lazy.render(self.alpha, self.overlay_alpha)



class Text(Component):
    fonts: dict[tuple[str, int], pg.font.Font] = {}
    
    @classmethod
    def loadFont(cls, path: str, size: int):
        ff = cls.fonts.get((path, size))
        if not ff: ff = cls.fonts[(path, size)] = pg.font.Font(f"assets/{path}.ttf", size)
        return ff

    def __init__(self, text: str = " ", color: RGB = Color.black, size = 14, antialias = False, path = "jb_semibold"):
        self.text = text
        self.color = color
        self.antialias = antialias
        self.fontdir = path, size
        self.font = Text.loadFont(path, size)
        self.alpha = 255
        self.c_hash = 0

    def after_init(self):
        self.lazy = LazySurface(self.transf)

    def update_render(self):
        if not self.lazy.unchanged or (self.c_hash != hash(self.text)):
            rendered = self.font.render(self.text, self.antialias, self.color)
            self.lazy.recreate(rendered, vec(rendered.get_size()))
            self.c_hash = hash(self.text)

        self.lazy.render(self.alpha)



@dataclass
class Blendkey:
    rgba: RGBA
    k: float

class ColorBlend:
    '''Pha từ một đống màu và key'''
    def __init__(self, keys: list[Blendkey]):
        self.keys = keys

    def interpolate(self, t) -> RGBA:
        if len(self.keys) == 1:
            k = self.keys[0]
            return k.rgba
        
        keys = self.keys
        # Bốc key nào phù hợp trong vùng r return
        # Sắp sai thứ tự ráng chịu
        for i in range(len(self.keys) - 1):
            k1, c1 = keys[i].k, keys[i].rgba
            k2, c2 = keys[i + 1].k, keys[i + 1].rgba
            
            if not (k1 <= t <= k2): continue
            if k1 == k2: return c1
            f = (t - k1) / (k2 - k1)
            # For thủ công :))
            return (
                int(c1[0] + (c2[0] - c1[0]) * f),
                int(c1[1] + (c2[1] - c1[1]) * f),
                int(c1[2] + (c2[2] - c1[2]) * f),
                int(c1[3] + (c2[3] - c1[3]) * f)
            )

        return self.keys[0 if (t < self.keys[0].k) else -1].rgba