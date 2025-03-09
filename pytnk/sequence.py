from .engine import *

class Sequence(Component):
    e_finished: Event['Sequence'] = Event()
    def __init__(self, animTime = 1.0):
        self.animTime = animTime

    def start(self):
        self.sinceStart = time()


class IntroSeq(Sequence):
    def __init__(self, splitLen = 200, **kwargs):
        super().__init__(**kwargs)
        self.splitLen = splitLen

    def start(self):
        super().start()
        self.logo = self.go.childs[0].transf
        self.logotext = self.go.childs[1].transf

    def update_logic(self):
        self.dt = time() - self.sinceStart
        if self.dt >= self.animTime:
            print("Finish intro")
            Sequence.e_finished.notify(self)
            self.go.destroy()
            return
        
        percent = 1 - math.sin(self.dt / self.animTime * DEGREE90)
        dist = (1 - percent * percent * percent) * self.splitLen
        self.logo.pos = dist * FORWARD
        self.logotext.pos = -dist * FORWARD

    def update_render(self):
        pass#self.canvas.blit(self.logo, App.native)


class LoadingSeq(Sequence):
    def __init__(self, cellsize = 50, waveLength = 10, **kwargs):
        super().__init__(**kwargs)
        self.cellsize = cellsize
        self.waveLength = max(waveLength, 1)
        self.dt = 0

        self.grid = (App.native[0] // cellsize, App.native[1] // cellsize)
        totalDiag = self.grid[0] + self.grid[1] - 1
        self.key = self.animTime / (totalDiag - 1 + self.waveLength)

    def update_logic(self):
        self.dt = time() - self.sinceStart
        if self.dt >= self.animTime:
            print("Start (actual) loading")
            Sequence.e_finished.notify(self)
            self.go.destroy()

    def update_render(self):
        for y in range(self.grid[1]):
            for x in range(self.grid[0]):
                self.renderCell(x, y, self.dt / self.key)

    def renderCell(self, x: int, y: int, dt: float):
        t_start = (x + y)
        percent = min(max(0, (dt - t_start) / self.waveLength), 1)

        size = percent * self.cellsize
        odd = (x + y) % 2
        color = (255, 255, 0) if odd else (255, 180, 0)
        center = vec(x + 0.5, y + 0.5) * self.cellsize
        topleft = center - vec(size) / 2
        pg.draw.rect(App.display, color, (topleft[0], topleft[1], size, size))