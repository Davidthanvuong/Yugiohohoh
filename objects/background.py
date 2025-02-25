from importer.gobj import *

class Background(Transform):
    def __init__(self):
        super().__init__(
            imgpath="fs_woodfloor_seemless.jpg", 
            imgsize=vec(NATIVE), pivot=vec(ZERO)
        )

    def update(self):
        render(self)