from pytnk.engine import *

class MonsterUI(Component):
    def __init__(self, attach: 'Monster', defWidth = 100):
        self.attach = attach
        self.barWidth = defWidth
        self.oldRatio = 1
        self.ratio = 1

    def start(self):
        self.defText = self.go.childs[0].getComponent(Text)
        self.atkText = self.go.childs[1].getComponent(Text)

    def update_logic(self):
        self.ratio = self.attach.defense / self.attach.maxDefense
        self.defText.text = str("%.0f" % self.attach.defense)
        # self.atkText.text = str(self.attach.attack)

    def update_render(self):
        # Blit primitive shape
        pg.draw.rect(App.display, Color.white,      (self.transf.g_pos, (self.barWidth * self.oldRatio, 10)))
        pg.draw.rect(App.display, Color.freedom,    (self.transf.g_pos, (self.barWidth * self.ratio, 10)))
        pg.draw.rect(App.display, Color.black,      (self.transf.g_pos, (self.barWidth, 10)), 2)

        self.oldRatio = (self.oldRatio * 10 + self.ratio) / (10 + 1)