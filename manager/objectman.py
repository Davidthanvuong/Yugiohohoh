from importer.gobj import *
from engine.fpscounter import *

from objects import *

class ObjectManager:
    def __init__(self):
        self.layers = [[] for _ in range(102)]
        Transform.setupPivot()

    def layer_add(self, layer: int, go: Transform):
        self.layers[layer].append(go)

    def load_mainGame(self):
        # Background
        self.layer_add(0, Background())

        # Entities
        for i in range(10):
            summon = Summon('guard', vec(CENTER[0] - 450 + 100 * i, CENTER[1]))
            self.layers[10].append(summon)

        self.layer_add(20, Player())

        # UI
        for i in range(10):
            pos = vec(100 + i * 50, NATIVE[1] - 150)
            card = Card(pos, pivot=vec(ZERO))
            self.layer_add(2, card)

        for i in range(10):
            pos = vec(NATIVE[0] - i * 50, 150)
            card = Card(pos, True, pivot=vec(ONE))
            self.layer_add(100, card)
        
        # Post processing
        self.layer_add(101, FPSCounter())

    # interpolate
    def obj_update(self):
        for layer in self.layers:
            for obj in layer:
                obj.update()

    # 20 frame
    def obj_logicupdate(self):
        pass