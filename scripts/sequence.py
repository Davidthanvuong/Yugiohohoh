from pytnk.engine import *

class IntroSeq(Component):
    def build(self):
        intro = Image('background\\yugioh_bg.jpg', App.native).build(pos=App.center).scope()
        devsText = Text('~~~ Tác giả ~~~', Color.white, 40).build(pos=(0, 200))

        authors = ["chad_1.jpg", "anya_2.jpg", "scout_3.png", "monster/amir.png"]
        [Image(authors[i], 128).build(pos=((i - 1.5) * 160, 300)) for i in range(4)]

        self.logo = Image('pytnk.png', 200).build(pos=(400, 0)).transf
        self.brand = Text('PyTNK Game Engine', size=40).build().transf
        return intro.unscope() + self

    def __init__(self, splitLen = 200, animTime = 1.0):
        self.motion = Motion.ease_out_cubic(vZERO, vec(splitLen, 0), animTime)
        self.waiting: No[Motion] = None
        
    def update_logic(self):
        if self.waiting and self.waiting.completed:
            StartMenu().build()
            return self.go.destroy()
        
        if (not self.waiting) and self.motion.completed:
            self.waiting = Motion.linear(0, 1, 0.5)
            return

        dist = self.motion.value
        self.logo.pos = dist
        self.brand.pos = -dist



class StartMenu(Component):
    def build(self):
        menu = Image('background\\willsmith.png', App.native).build(pos=App.center).scope()
        st = Image('pytnk.png', (200, 100)).build() + Text('Start Game', Color.white, 40)
        return menu.unscope() + self
    
    def update_logic(self):
        if Mouse.clicked:
            LoadingSeq().build()
            return self.go.destroy()
        


class LoadingSeq(Component):
    def build(self):
        loading = Image('background\\willsmith.png', App.native).build(anchor=TOPLEFT)
        return loading + self

    def __init__(self, cellsize = 50, waveLength = 15, animTime = 1.2):
        self.cellsize = cellsize
        self.waveLength = max(waveLength, 1)
        self.grid = (App.native[0] // cellsize, App.native[1] // cellsize)
        self.interval = (self.grid[0] + self.grid[1] - 2 + self.waveLength)
        self.motion = Motion.linear(0, self.interval, animTime)

    def update_logic(self):
        if self.motion.completed:
            Maingame_beginSeq().build()
            return self.go.destroy()

    def update_render(self):
        dt = self.motion.value
        for y in range(self.grid[1]):
            for x in range(self.grid[0]):
                self.renderCell(x, y, dt)

    def renderCell(self, x: int, y: int, dt: float):
        percent = min(max(0, (dt - (x + y)) / self.waveLength), 1)

        size = percent * self.cellsize
        color = (255, 200, 0) if (x + y) % 2 else (200, 160, 0)
        center = vec(x + 0.5, y + 0.5) * self.cellsize
        topleft = center - vec(size) / 2
        pg.draw.rect(App.screen, color, (topleft[0], topleft[1], size, size))



class Maingame_beginSeq(Component):
    def build(self):
        main = GameObject(pos=App.center, scale=(0.4, 0.4), rot=90).scope()
        self.human1 = Image('human.png', size=(500, 300)).build(scale=(2, 2), pos=(0, 1000)).transf
        self.human2 = Image('human.png', size=(500, 300)).build(scale=(2, 2), rot=180, pos=(0, -1000)).transf

        table = Image('background\\woodfloor.jpg', (App.native[0], App.native[1] - 200)).build(pos=100 * UPWARD)
        plank = Image('background\\wood.jpg', (App.native[0], 200)).build(pos=(0, App.center[1] - 100))

        self.coin = Image('doge.png', (256, 256), True).build(startEnabled=False).transf

        return main.unscope() + self
    
    def __init__(self):
        self.action = self.sequence()

    def update_logic(self):
        if self.action:
            try: next(self.action)
            except StopIteration: self.action = None

    def sequence(self, walkTime = 0.8, tossTime = 1.0, tossAmount = 9, tossHeight = 500.0):
        walk = Motion.ease_out(1000, 700, walkTime)
        zoom = Motion.linear(vec(0.5), vec(1), walkTime).bind(self.transf, 'scale')
        rotate = Motion.linear(90, 0, walkTime).bind(self.transf, 'rot')
        while not walk.completed:
            self.human1.pos.y = walk.value
            self.human2.pos.y = -walk.value
            yield
        
        self.coin.go.enabled = True
        notmyluck = True if rint(0, 1) else False
        tossing = Motion.linear(0, tossAmount + notmyluck, tossTime)
        tossUp = Motion.ease_in(0, -tossHeight, tossTime, False, True)
        while not tossing.completed:
            self.coin.scale.y = 1 - abs(tossing.value % 2.0 - 1) * 2
            self.coin.pos.y = tossUp.value
            yield

        self.coin.scale.y = 1 - notmyluck * 2
        img = self.coin.go.getComponent(Image)
        opacity = Motion.ease_out(255, 0, 0.5).bind(img, 'overlay_alpha')
        while not opacity.completed: yield

        from .maingame import Maingame
        Maingame().build(notmyluck)
        self.go.destroy()