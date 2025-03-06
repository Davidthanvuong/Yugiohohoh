from .header_pygame import *

class Menu(Component):
    def __init__(self, editor = "", minSize: tff = (200, 32), **kwargs):
        super().__init__(**kwargs)
        self.minSize = minSize
        if editor != "":
            Window.EditorsName.append(editor)

    def __call__(self):
        Window.e_onDisplayChange += self.onSizeChanged
        self.currSize = self.go.hitbox

    def onSizeChanged(self):
        self.go.scene.buffer = pg.Surface(self.go.hitbox, pg.SRCALPHA)