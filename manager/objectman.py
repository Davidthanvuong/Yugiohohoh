from importer.gobj import *
from engine.fpscounter import *

from objects import *
import time

class ObjectManager:
    def __init__(self):
        self.scenes = [[[] for _ in range(102)]]
        #Transform.setupPivot()

    def add(self, layer: int, go: Transform, scene: int = 0):
        self.scenes[scene][layer].append(go)

    def load_loadingScene(self):
        self.scenes.append([[] for _ in range(10)])
        print("Loading. Simulating loading screen")
        self.add(0, LoadingBackground(), scene=1)
        print("Loaded")
        del self.scenes[1]

    def load_mainGame(self):
        self.add(0, Background())

        for i in range(10):
            summon = Summon('guard', vec(CENTER[0] - 450 + 100 * i, CENTER[1]))
            self.add(1, summon)

        self.add(20, Player())

        for i in range(10):
            pos = vec(100 + i * 50, NATIVE[1] - 150)
            card = Card(pos, pivot=vec(ZERO))
            self.add(2, card)

        for i in range(10):
            pos = vec(NATIVE[0] - i * 50, 150)
            card = Card(pos, True, pivot=vec(ONE))
            self.add(90, card)
        
        self.add(91, FPSCounter())

    def obj_update(self):
        for scene in self.scenes:
            for layer in scene:
                for obj in layer:
                    obj.update()

    def obj_logical_update(self):
        pass