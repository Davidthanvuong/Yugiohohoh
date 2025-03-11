from .engine import *

class IntroSeq(Component):
    @staticmethod
    def create_default(**kw):
        intro = GameObject("Intro", pos=App.center, toScope=True)
        intro += Image('background\\yugioh_bg.jpg', App.native)

        logo  = GameObject("Logo") + Image('icon\\pytnk.png', (200, 200))
        brand = GameObject("Brand") + Text('PyTNK Game Engine', color=Color.black, size=40)
        intro += IntroSeq(logo, brand, **kw)

        devsText = GameObject('Author', pos=(0, 200))
        devsText += Text('~~~ Tác giả ~~~', color=Color.black, size=40)
        for i in range(4):
            dev = GameObject(f'Dev {i}', pos=((i - 1.5) * 160, 300))
            dev += Image("icon\\white.png", size=(128, 128))
    
        intro.unscope()
        return intro
    
    def __init__(self, logo: GameObject, brand: GameObject, splitLen = 200, animTime = 1.0):
        self.logo = logo.transf
        self.brand = brand.transf
        self.motion = Motion.ease_out_cubic(0, splitLen, animTime)

    def update_logic(self):
        if self.motion.completed:
            StartMenu.create_default()
            return self.go.destroy()

        dist = self.motion.value
        self.logo.pos = dist * FORWARD
        self.brand.pos = -dist * FORWARD



class StartMenu(Component):
    @staticmethod
    def create_default(**kw):
        menu = GameObject('Start Menu', anchor=TOPLEFT)
        menu += Image('background\\willsmith.png', App.native)
        menu += StartMenu(**kw)

        button = GameObject('Start Button', menu, pos=App.center, anchor=CENTER)
        button += Image('icon\\pytnk.png', (200, 100))
        button += Text('Start Game', color=Color.black, size=40)

        return menu

    def update_logic(self):
        if Mouse.clicked:
            LoadingSeq.create_default()
            return self.go.destroy()



class LoadingSeq(Component):
    @staticmethod
    def create_default(**kw):
        loading = GameObject('Loading Scene', anchor=TOPLEFT)
        loading += Image('background\\willsmith.png', App.native)
        loading += LoadingSeq(**kw)
        return loading

    def __init__(self, cellsize = 50, waveLength = 10, animTime = 1.5):
        self.cellsize = cellsize
        self.waveLength = max(waveLength, 1)
        self.grid = (App.native[0] // cellsize, App.native[1] // cellsize)
        self.interval = (self.grid[0] + self.grid[1] - 2 + self.waveLength)
        self.motion = Motion.linear(0, 1, animTime)

    def update_logic(self):
        if self.motion.completed:
            Maingame_beginSeq.create_default()
            return self.go.destroy()

    def update_render(self):
        dt = self.motion.value
        for y in range(self.grid[1]):
            for x in range(self.grid[0]):
                self.renderCell(x, y, dt * self.interval)

    def renderCell(self, x: int, y: int, dt: float):
        percent = min(max(0, (dt - (x + y)) / self.waveLength), 1)

        size = percent * self.cellsize
        color = (255, 200, 0) if (x + y) % 2 else (200, 150, 0)
        center = vec(x + 0.5, y + 0.5) * self.cellsize
        topleft = center - vec(size) / 2
        pg.draw.rect(App.screen, color, (topleft[0], topleft[1], size, size))



class Maingame_beginSeq(Component):
    @staticmethod
    def create_default():
        vertical_pos = vec((App.center[0] - App.center[1]) / App.iv_ratio, App.native[1])

        main = GameObject('Maingame Scene', anchor=TOPLEFT, toScope=True,
                          pos=vertical_pos, scale=(App.iv_ratio, App.iv_ratio), rot=90)
        main += Image('background\\woodfloor.jpg', (App.native[0], App.native[1] - 200))

        human1 = GameObject('Human 1', pos=(App.center[0], -250), scale=(3, 3), rot=180) + Image("human.png", size=(500, 180))
        human2 = GameObject('Human 2', pos=(App.center[0], App.native[1] + 250), scale=(3, 3)) + Image("human.png", size=(500, 180))
        
        plank = GameObject('Board', pos=(0, App.native[1] - 200), anchor=TOPLEFT)
        plank += Image('background\\wood.jpg', (App.native[0], 200))

        coin = GameObject('Coin', pos=(App.center[0], App.center[1] // 2), anchor=CENTER)
        coin += Image('doge.png', (256, 256), notLazy=True)

        main += Maingame_beginSeq(human1, human2, coin)
        # main += BattleController()
        main.unscope()
        return main

    def __init__(self, human1: GameObject, human2: GameObject, coin: GameObject, 
                 zoomTime = 1.0, walkTime = 0.8, tossTime = 0.6):
        self.human1 = human1.transf
        self.human2 = human2.transf
        self.coin = coin.transf
        self.coinImg = coin.getComponent(Image)

        self.walkTime = walkTime
        self.zoomTime = zoomTime
        self.tossTime = tossTime

        self.finishedWalk = False
        self.startedZoom = False
        self.finishedZoom = False
        self.finishedToss = False
        self.walking = Motion.ease_out(250, 600, walkTime)

    def update_logic(self):
        if not self.finishedWalk:
            self.walk_motion()

        if self.startedZoom and not self.finishedZoom:
            self.zoom_motion()

        if self.finishedZoom and not self.finishedToss:
            self.toss_coin()

        if self.finishedToss:
            self.toss_fading()

    def walk_motion(self):
        move = self.walking.value
        self.human1.pos.y = -move
        self.human2.pos.y = App.native[1] + move

        if self.walking.t >= 0.3 and not self.startedZoom:
            self.startedZoom = True
            print(f"Started zoom {now()}")
            self.zoom       = Motion.ease_in(0, 1, self.zoomTime)
            self.motion     = Motion.ease_in(self.transf.pos, vZERO, self.zoomTime)
            self.scaling    = Motion.ease_in(vec(App.iv_ratio), vONE, self.zoomTime)

        if self.walking.completed:
            print(f"Walking completed {now()}")
            self.finishedWalk = True

    def zoom_motion(self):
        if self.zoom.completed and not self.finishedZoom:
            self.transf.rot = 0
            self.transf.pos = vZERO
            self.transf.scale = vONE
            self.finishedZoom = True
            self.toss = Motion.linear(0, rint(5, 6), self.tossTime)

            print("[TODO] Start game text here")
            print(f"Zoom completed {now()}")
            return

        dt = self.zoom.value
        self.transf.rot = (1 - dt) * 90
        self.transf.pos = self.motion.value
        self.transf.scale = self.scaling.value

    def toss_coin(self):
        if self.toss.completed:
            opponent_startFirst = self.coin.rot == 180
            print(opponent_startFirst)
            Maingame.create_default(opponent_startFirst)
            self.fadeMotion = Motion.ease_in(255, 0, 1.0)
            self.finishedToss = True
            return
        
        self.coin.scale.y = self.toss.value % 1
        self.coin.rot = (int(self.toss.value) % 2) * 180

    def toss_fading(self):
        if self.fadeMotion.completed:
            self.activated = False
            self.coinImg.shared.native.set_alpha(255)
            del self.coinImg
            self.coin.go.destroy()
            return
        
        self.coinImg.shared.native.set_alpha(self.fadeMotion.value)