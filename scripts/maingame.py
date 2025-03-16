from pytnk.engine import *

class Maingame(Component):
    userCount = 2
    userType: list[type[Controller]] = [PlayerController, BotController]

    def build(self, startID: int):
        mg = Image('background\\woodfloor.jpg', (App.native[0], App.native[1] - 200)).build(anchor=TOPLEFT).scope()
        plank = Image('background\\wood.jpg', (App.native[0], 200)).build(pos=(0, App.native[1]), anchor=BOTTOMLEFT)

        self.mgImg = mg.getComponent(Image)
        self.plankImg = plank.getComponent(Image)

        self.ended = 0
        self.users: list[Controller] = []
        for i in range(0, self.userCount):
            self.users.append(self.userType[i](self).build(i))

        self.users[0].opponent = self.users[1]
        self.users[1].opponent = self.users[0]

        self.notif = PhaseIndicator().build()

        self.users[startID].e_start_drawPhase.notify()
        return mg + self
    
    def __init__(self, scopeZoom = 2.0):
        self.zooming: No[Generator] = None
        self.scopeZoom = scopeZoom
        self.scopeIn = False
    
    def update_logic(self):
        if CardSlot.dragging:
            if not self.scopeIn:
                self.transf.scale = vec(self.scopeZoom)
                self.mgImg.activated = False
                self.plankImg.activated = False
                self.scopeIn = True
            self.transf.pos = (self.transf.scale - vONE).elementwise() * -Mouse.pos
        elif self.scopeIn:
            self.scopeIn = False
            self.transf.scale = vONE
            self.transf.pos = vZERO
            self.mgImg.activated = True
            self.plankImg.activated = True

    def drawCard_time(self):
        for user in self.users:
            user.draw_time()
        

class PhaseIndicator(Component):
    def build(self):
        img = Image('background\\fade_up.png', (App.native[0], self.phaseHeight)).build(pos=(App.center[0], 0), startEnabled=False)
        self.text = img.addComponent(Text('Sample text', Color.white, 60))
        self.img = img.getComponent(Image)
        return img.addComponent(self)
    
    def __init__(self, glideSpeed = 0.3, fadeSpeed = 0.5, phaseHeight = 300):
        self.glideSpeed = glideSpeed
        self.fadeSpeed = fadeSpeed
        self.phaseHeight = phaseHeight
        self.action: No[Generator] = None

    def update_logic(self):
        if self.action:
            try: next(self.action)
            except StopIteration: self.action = None

    def startNotif(self, side: int, text: str):
        self.go.enabled = True
        self.text.text = text
        half = self.phaseHeight / 2
        if side:
            self.motion = Motion.ease_out(-half, half, self.glideSpeed)
            self.transf.pos.y = -half
            self.transf.rot = 180
        else:
            self.motion = Motion.ease_out(App.native[1] + half, App.native[1] - half, self.glideSpeed)
            self.transf.pos.y = App.native[1] + half
            self.transf.rot = 0
        
        self.action = self.gliding()

    def gliding(self):
        self.img.alpha = 255
        self.text.alpha = 255
        while not self.motion.completed:
            self.transf.pos.y = self.motion.value
            yield
        
        fade = Motion.ease_in_cubic(255, 0, self.fadeSpeed)
        while not fade.completed:
            self.img.alpha = fade.value
            self.text.alpha = fade.value
            yield

        self.go.enabled = False