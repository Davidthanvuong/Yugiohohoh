from .gameobjects import *

class GOManager:
    def __init__(self):
        self.layers = [[] for _ in range(102)]

    def load_mainGame(self):
        # Background
        self.layers[0].append(Background())

        # Entities
        for i in range(10):
            summon = Summon('guard', vec(CENTER[0] - 450 + 100 * i, CENTER[1]))
            self.layers[10].append(summon)

        self.layers[20].append(Player())

        # UI
        for i in range(10):
            pos = vec(100 + i * 50, NATIVE[1] - 150)
            card = Card(pos)
            self.layers[2].append(card)

        for i in range(10):
            pos = vec(NATIVE[0] - i * 50, 150)
            card = Card(pos, True)
            card.image.pivot = vec(1, 1)
            self.layers[90].append(card)
        
        # Post processing
        self.layers[101].append(FPSCounter())

    def obj_update(self):
        for layer in self.layers:
            for obj in layer:
                obj.update()