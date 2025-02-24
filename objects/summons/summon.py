from importer.gobj import *

class Summon(Transform, IClickable):
    classes = {
        'guard': "summon\\guard.png"
    }

    def __init__(self, role: str, pos: vec = vec(CENTER)):
        self.velY = 0
        self.role = role
        self.body = Imager(Summon.classes[self.role], size=vec(150, 350), pivot=vec(0.5, 1), parent=self)
        super().__init__(pos, host=self.body)

    def update(self):
        self.iclickable_update()
        render(self.body, self.pos)