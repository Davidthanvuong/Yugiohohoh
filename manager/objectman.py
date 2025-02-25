from importer.gobj import *
from engine.fpscounter import *

from objects import *

class ObjectManager:
    def __init__(self):
        self.scenes = [[[] for _ in range(102)]]

    def add(self, layer: int, go: Transform, scene: int = 0):
        self.scenes[scene][layer].append(go)

    def load_mainGame(self):
        self.add(0, Background())

        for i in range(10):
            summon = Summon('guard', vec(CENTER[0] - 450 + 100 * i, CENTER[1]))
            self.add(1, summon)

        self.add(20, Player())
        self.add(25, CardDeck(pos=vec(200, NATIVE[1] - 200), pivot=vec(0, 0)))
        self.add(25, CardDeck(pos=vec(NATIVE[0] - 1100, -100), pivot=vec(0, 0), back=True))
        
        self.add(91, FPSCounter())

    def obj_update(self):
        for scene in self.scenes:
            for layer in scene:
                for obj in layer:
                    obj.update()

    def obj_logical_update(self):
        pass