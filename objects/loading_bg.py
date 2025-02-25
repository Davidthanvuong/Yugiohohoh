from importer.gobj import *

class LoadingBackground(Transform):
    def __init__(self):
        super().__init__(
            imgpath="loading.jpg", 
            imgsize=vec(NATIVE), pivot=vec(0, 0)
        )

    def update(self):
        render(self)