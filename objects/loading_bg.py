from importer.gobj import *

class LoadingBackground(Transform):
    def __init__(self):
        super().__init__(
            imgpath="loading.jpg", 
            imgsize=vec(NATIVE), pos=vec(CENTER)
        )

    def update(self):
        render(self)