from pytnk.engine import *

class PlayerController(Controller):
    '''Cho phép người chơi tương tác'''
    def build(self, *a):
        ret = super().build(name="Player", *a)
        endButton = My_EndPhaseButton(self).build()
        return ret

    def __init__(self, *a):
        super().__init__(*a)
        self.rightSide = False
        self.isPlayer = True

    def hear_start_drawPhase(self):
        super().hear_start_drawPhase()
        print("[Player] MY TURN")



class My_EndPhaseButton(IClickable):
    def build(self):
        bottom = (App.native[0] - 20, App.native[1] - 50)
        button = Image("white.png", (200, 40), override_hitbox=True)\
                    .build(parent=self.user.go, pos=bottom, anchor=BOTTOMRIGHT, startEnabled=False)\
                    + Text("End", Color.black, 20)
        return button + self

    def __init__(self, user: Controller):
        super().__init__()
        self.user = user
        user.e_start_drawPhase += self.reEnable

    def reEnable(self):
        self.go.enabled = True

    def after_init(self):
        self.com_image = self.go.getComponent(Image)
        self.com_text = self.go.getComponent(Text)

    def update_logic(self):
        additional = f"({self.user.placeCard_left}, {self.user.quickAction_left})"
        self.com_text.text = "End Phase " + additional

    def on_startClick(self):
        self.user.e_end_drawPhase.notify()
        self.go.enabled = False