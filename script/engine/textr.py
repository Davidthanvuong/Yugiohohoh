from .imager import *
from .abstract_renderer import *

class Textr(Imager):
    def __init__(self, **kwargs):
        self.fonter = pg.font.Font("Comic.ttf", 20)
        self.color = pg.Color(255, 255, 255)

        img = self.fonter.render("Text", True, self.color) # Workaround
        super().__init__(sf=img, pivot=vec(0, 0), **kwargs)

    def write(self, text: str, parent: vec):
        img = self.fonter.render(text, True, self.color)
        self.size = vec(img.get_size())
        del self.shared
        self.shared = ImageCache(img)
        render(self, parent)