from importer.pygame import *
from .imagecache import ImageCache
from .transform import Imager
from .abstract_renderer import render

class Textr(Imager):
    def __init__(self, **kwargs):
        super().__init__(pivot=vec(0, 0), **kwargs)
        self.fonter = pg.font.Font("Comic.ttf", 20)
        self.color = pg.Color(255, 255, 255)

    def write(self, text: str, parent: vec):
        img = self.fonter.render(text, True, self.color)
        self.size = vec(img.get_size())
        #del self.shared
        self.shared = ImageCache(img)
        render(self, parent)