from ..engine.gameobject import *

class Summon(GameObject):
    classes = {
        'guard': "summon\\guard.png"
    }

    def __init__(self, role: str, pos: vec = vec(CENTER)):
        super().__init__(pos)
        self.velY = 0
        self.role = role
        self.body = Imager(Summon.classes[self.role], size=vec(150, 350), pivot=vec(0.5, 1))

    def update(self):
        render(self.body, self.pos)