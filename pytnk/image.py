from .header_pygame import *

pg.font.init()

class SharedImage:
    '''Load & lưu Texture động (dynamically) vào bộ nhớ, khi nào cần lấy ra'''
    database: dict[int, 'SharedImage'] = {}
    
    def __init__(self, path: str = ""):
        if path == "":
            self.texture = pg.Surface((0, 0), pg.SRCALPHA)
        else:
            self.texture = pg.image.load(f"assets\\images\\{path}").convert_alpha()
        self.gl_texture = None

        self.cached = self.texture
        self.last_grot = 0.0
        self.last_px_gscale = vec(ZERO)
        self.topleft = vec(ZERO)
        # if bh != 0:
        #     self.helllist: list[pg.Surface] = [] * (360 // bh)

    @classmethod
    def fetch(cls, path: str):
        '''Cố gắng Load texture và OpenGL texture từ bộ nhớ, không có thì tạo cái mới'''        
        poly = hash(path)
        if poly not in cls.database:
            cls.database[poly] = SharedImage(path)

        return cls.database[poly]


class Renderer(Component):
    '''Class để trừu tượng hóa việc render. PyOpenGL (optional) sẽ được import ở thư viện ngoài'''
    def __init__(self, fit = False, indent = 0, **kwargs):
        super().__init__(**kwargs)
        self.fit = fit                  # Tự canh theo hitbox
        self.indent = indent            # Thục vào trong size một khoảng


    def get_calibration(self, rect_size: tff):
        '''Tự calibrate từ rect_size, trả về vị trí offset đúng với pivot'''
        pass




class Image(Renderer):
    '''Ảnh được cập nhật lười. 
    fit=True để tự động chỉnh theo hitbox
    standalone=True nếu ảnh là riêng biệt
    bullethell=True nếu dùng cho rất nhiều projectile và nhiều góc xoay'''

    def __init__(self, path: str = "", size: No[tff] = None, useScale = False, standalone = False, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.standalone = standalone
        # Nếu là standalone thì không lưu vô database hay share
        self.cache = SharedImage(path) if standalone else SharedImage.fetch(path)
        self.size = vec(size if size else self.cache.texture.get_size())
        #todo: useScale

        self.changed = False


    def __getstate__(self):
        '''Lưu vật đến pickle'''
        state = self.__dict__.copy()
        state.pop("cache", None)        # Không thể serialize ảnh (ko sao cả)
        return state
    

    def __setstate__(self, state):
        '''Đọc vật từ pickle'''
        self.__dict__.update(state)
        self.changed = True

        if self.standalone:
            self.cache = SharedImage(self.path)
        else:
            self.cache = SharedImage.fetch(self.path)

        
    def update_logic(self):
        if self.fit: self.size = self.tf.hitbox


    def update_render(self):
        tf, ct = self.tf, self.cache
        grot = tf.global_angle
        px_gscale = (self.size - vec(ONE) * self.indent).elementwise() * tf.global_scale

        if self.changed or ((not tf.no_angle) and ct.last_grot != grot) or (ct.last_px_gscale != px_gscale):
            #print("Regenerate", self.changed, tf.no_angle, ct.last_grot, grot, ct.last_px_gscale, px_gscale)
            sf = ct.texture # Lấy ảnh gốc
            if px_gscale != vec(sf.get_size()): sf = pg.transform.scale(sf, px_gscale)
            if (not tf.no_angle) and grot != 0: sf = pg.transform.rotate(sf, -grot)

            # Lưu cache lại một đống tham số đánh dấu và dữ liệu
            ct.last_grot = grot
            ct.last_px_gscale = px_gscale
            ct.topleft = (px_gscale.elementwise() * (CENTER - tf.pivot)).rotate(grot) # Đừng bỏ dấu ngoặc ra
            ct.cached = sf
            self.changed = False
        else:
            sf = ct.cached

        rect = sf.get_rect(center = tf.global_pos + ct.topleft - self.tf.root[0].pos)
        tf.root[1].blit(sf, rect)




class Text(Renderer):
    '''Ghi chữ có tiện ích ở đây'''
    fonts: Final[dict[str, pg.font.Font]] = {
        'comic': pg.font.Font("assets\\Comic.ttf", 14),
        'jetbrain': pg.font.Font("assets\\Comic.ttf", 14),
        'jetbrains_big': pg.font.Font("assets\\jetbrains_semibold.ttf", 30),
        'jetbrains_massive': pg.font.Font("assets\\jetbrains_semibold.ttf", 60)
    }

    def __init__(self, text: str = "", color = colormap['white'],
                 preset = 'comic', **kwargs):
        super().__init__(**kwargs)
        #self.fontsize = preset
        self.preset = preset
        self.writer = Text.fonts[preset]
        self.text = text
        self.old_hash = hash(text)
        self.color = color

        self.cache_id = 0
        self.cached_text = pg.Surface((0, 0))
        self.last_grot = 0.0
        self.last_gscale = vec(ZERO)
        self.pixels = vec(ZERO)
        self.topleft = vec(ZERO)
    

    def update_logic(self):
        if hash(self.text) != self.old_hash:
            self.changed = True
            self.old_hash = hash(self.text)


    def update_render(self):
        tf = self.tf
        grot = tf.global_angle
        gscale = tf.global_scale

        isDifferentRect = (not tf.no_angle and (self.last_grot != grot)) or (self.last_gscale != gscale)
        if isDifferentRect or (hash(self.text) != self.cache_id):
            #print(f"{self.tf.name}'s text changed: {self.last_grot}!={grot} {self.last_gscale}!={gscale} {hash(self.text)}!={self.cache_id}")
            sf = self.writer.render(self.text, True, self.color)
            self.last_gscale = gscale
            self.pixels = vec(sf.get_size()).elementwise() * gscale

            if (not tf.no_angle) and grot != 0: sf = pg.transform.rotate(sf, -grot)
            if gscale != vec(ONE): sf = pg.transform.scale(sf, self.pixels)

            # Lưu cache lại một đống tham số đánh dấu và dữ liệu
            self.last_grot = grot
            self.last_gscale = gscale
            self.topleft = (self.pixels.elementwise() * (CENTER - tf.pivot)).rotate(grot) # Đừng bỏ dấu ngoặc ra
            self.cached_text = sf
            self.cache_id = hash(self.text)
        else:
            sf = self.cached_text

        rect = sf.get_rect(center = tf.global_pos + self.topleft - self.tf.root[0].pos)
        tf.root[1].blit(sf, rect)


    def __getstate__(self):
        '''Lưu vật đến pickle'''
        state = self.__dict__.copy()
        state.pop("writer", None)        # Không thể serialize ảnh (ko sao cả)
        state.pop("cached_text", None)
        return state
    

    def __setstate__(self, state):
        '''Đọc vật từ pickle'''
        self.__dict__.update(state)
        self.writer = Text.fonts[self.preset]
        self.cache_id = 0