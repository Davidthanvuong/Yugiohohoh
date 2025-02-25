from importer.gobj import *

class Summon(Transform):
    classes = {
        'guard': "summon\\guard.png"
    }

    def __init__(self, role: str, pos: vec = vec(CENTER)):
        self.velY = 0
        self.role = role
        super().__init__(
            imgpath=Summon.classes[self.role],
            imgsize=vec(150, 350), 
            pos=pos, pivot=vec(0.5, 1))

    def update(self):
        #self.iclickable_update()
        render(self)