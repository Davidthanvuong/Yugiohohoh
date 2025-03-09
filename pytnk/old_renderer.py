# from .engine import *


# class SharedImg:
#     img_db: dict[str, 'SharedImg'] = { }
#     font_db: dict[tuple[str, int], Font] = {}

#     '''Load & lưu Texture động (dynamically) vào bộ nhớ, khi nào cần lấy ra'''
#     def __init__(self, path: str, expected: tff = ZERO, small: tff = ZERO):
#         self.native = pg.image.load(f"assets\\images\\{path}").convert_alpha()
#         if expected != ZERO:
#             self.native = pg.transform.scale(self.native, expected)

#         self.smallSize = vec(small)
#         self.smallImg = pg.transform.scale(self.native, small)

#     @classmethod
#     def getImage(cls, path: str, size: tff = ZERO):
#         sh = cls.img_db.get(path)
#         if not sh: 
#             sh = cls.img_db[path] = cls(path, size)
#         return sh
    
#     @classmethod
#     def getFont(cls, path: str, size: int):
#         ff = cls.font_db.get((path, size))
#         if not ff:
#             ff = cls.font_db[(path, size)] = pg.font.Font(f"assets\\{path}.ttf", size)
#         return ff
    

# class Renderer(Component, pg.sprite.DirtySprite):
#     def __init__(self, canvas = None, pivot: tff = CENTER, notLazy = False):
#         #self.canvas = canvas if canvas else App.display
#         self.notLazy = notLazy
#         self.pivot = vec(pivot)

#         self.image = pg.Surface((0, 0))
#         self.rect = pg.Rect(0, 0, 0, 0)
#         self.dirty = 1

#         self.c_pos = vec(ZERO)
#         self.c_rot = 0.0
#         self.c_scale = vec(ZERO)
#         self.c_pixels = vec(ZERO)
#         self.c_topleft = vec(ZERO)

#     def render_lazy(self, f_getSf):
#         lazyImg = (self.c_rot == self.transf.g_rot) and (self.c_scale == self.transf.g_scale)
#         lazyBlit = not self.notLazy and self.dirty and lazyImg and (self.c_pos == self.transf.g_pos)

#         if not lazyImg:
#             # Chỉ update lại ảnh (local) khi thay đổi kích thước hoặc góc xoay
#             oldSf, imgsize = f_getSf()
#             self.c_rot = self.transf.g_rot
#             self.c_scale = self.transf.g_scale.copy()
#             self.c_pixels = self.c_scale.elementwise() * imgsize

#             sf = pg.transform.scale(oldSf, self.c_pixels)
#             if -1.0 <= self.c_rot <= 1.0: sf = pg.transform.rotate(sf, self.transf.g_rot)

#             self.image = sf
#             self.c_topleft = (self.c_scale.elementwise() * (CENTER - self.pivot)).rotate(self.c_rot)

#         if not lazyBlit:
#             # Chỉ render ảnh (lười) khi vị trí trong canvas bị thay đổi
#             self.dirty = True
#             self.c_pos = self.transf.g_pos
#             self.rect = self.image.get_rect(center = self.c_pos + self.c_topleft)
#             self.canvas.blit(self.image, self.c_pos)
    
#     def __getstate__(self):
#         state = self.__dict__.copy()
#         state.pop("c_surface", None)
#         return state
    
#     def __setstate__(self, state):
#         self.__dict__.update(state)
#         self.dirty = False
#         self.image = pg.Surface((0, 0))



# class Image(Renderer):
#     '''Ảnh được cập nhật lười'''

#     def __init__(self, path: str = "", size: tff = ZERO, **kwargs):
#         super().__init__(**kwargs)
#         self.path = path
#         self.shared = SharedImg.getImage(path, size)
#         self.imgsize = vec(size if size == ZERO else self.shared.native.get_size())

#     def getDefaultSf(self):
#         canGetSmall = self.imgsize.elementwise() < self.shared.smallSize.elementwise()
#         sf = self.shared.smallImg if canGetSmall else self.shared.native
#         return sf, self.imgsize

#     def update_render(self):
#         self.render_lazy(self.getDefaultSf)
    
#     def __getstate__(self):
#         state = self.__dict__.copy()
#         state.pop("shared", None)
#         return state
    
#     def __setstate__(self, state):
#         self.__dict__.update(state)
#         self.c_updated = False
#         self.shared = SharedImg.getImage(self.path)



# class Text(Renderer):
#     '''Tiện ích viết chữ'''

#     def __init__(self, text: str = "", color = Color.white, path = "jb_semibold", size = 14, **kwargs):
#         super().__init__(**kwargs)
#         self.font = SharedImg.getFont(path, size)
#         self.fontdir = path, size
#         self.text = text
#         self.old_hash = hash(text)
#         self.color = color

#     def __getstate__(self):
#         state = self.__dict__.copy()
#         state.pop("font", None)
#         return state
    
#     def __setstate__(self, state):
#         self.__dict__.update(state)
#         self.c_updated = False
#         self.font = SharedImg.getFont(self.fontdir[0], self.fontdir[1])

#     def getNew_textRender(self):
#         sf = self.font.render(self.text, False, self.color)
#         return sf, sf.get_size()

#     def update_render(self):
#         self.render_lazy(self.getNew_textRender)

# # class Text(Renderer):
# #     '''Ghi chữ có tiện ích ở đây'''

# #     def __init__(self, text: str = "", color = Color.white, path = "jb_semibold", size = 14, **kwargs):
# #         super().__init__(**kwargs)
# #         #self.fontsize = preset
# #         self.font = SharedImg.getFont(path, size)
# #         self.fontsize = size
# #         self.text = text
# #         self.old_hash = hash(text)
# #         self.color = color

# #         self.cache_id = 0
# #         self.cached_text = pg.Surface((0, 0))
# #         self.last_grot = 0.0
# #         self.last_gscale = vec(ZERO)
# #         self.pixels = vec(ZERO)
# #         self.topleft = vec(ZERO)
    
# #     def __getstate__(self):
# #         state = self.__dict__.copy()
# #         state.pop("cached_text", None)
# #         return state
    
# #     def __setstate__(self, state):
# #         self.__dict__.update(state)
# #         self.cache_id = 0

# #     def update_render(self):
# #         if hash(self.text) != self.old_hash:
# #             self.changed = True
# #             self.old_hash = hash(self.text)