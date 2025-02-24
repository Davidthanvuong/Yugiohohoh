from ..go_importer import *

class Background(GameObject):
    def __init__(self):
        super().__init__()
        self.image = Imager("fs_woodfloor_seemless.jpg", 
                            size=vec(1600, 1000), pivot=vec(0, 0))

    def update(self):
        render(self.image)