from pytnk.engine import *

class MonsterUI(Component):
    @staticmethod
    def create(attach: 'Monster'):
        ui = GameObject("Monster UI", attach.go, pos=(-50, 0))

        health = GameObject('1', ui, pos=(0, 0), anchor=MIDLEFT) 
        health += Image("icon\\heart.png", (20, 20))
        health += Text("0?", size=16)

        attack = GameObject('2', ui, pos=(20, 20), anchor=MIDLEFT)
        attack += Image("icon\\sword.png", (40, 40))
        attack += Text("0?", size=16)

        ui += MonsterUI(attach)
        return ui

    def __init__(self, attach: 'Monster', defWidth = 100):
        self.barWidth = defWidth
        self.oldRatio = 1
        self.ratio = 1
        self.attach = attach

    def after_init(self):
        self.defText = self.go.childs[0].getComponent(Text)
        self.atkText = self.go.childs[1].getComponent(Text)

    def update_logic(self):
        self.ratio = self.attach.defense / self.attach.maxDefense
        self.defText.text = str("%.0f" % self.attach.defense)
        self.atkText.text = str(self.attach.attack)

    def update_render(self):
        # Blit primitive shape
        pg.draw.rect(App.screen, Color.white,      (self.transf.g_pos, (self.barWidth * self.oldRatio, 10)))
        pg.draw.rect(App.screen, Color.freedom,    (self.transf.g_pos, (self.barWidth * self.ratio, 10)))
        pg.draw.rect(App.screen, Color.black,      (self.transf.g_pos, (self.barWidth, 10)), 2)

        self.oldRatio = (self.oldRatio * 10 + self.ratio) / (10 + 1)