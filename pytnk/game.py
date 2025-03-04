from .header_pygame import *
import time


class Game(Component):
    '''Za warudo! :insert_ngưng_động_thời_gian: :penguin:'''
    inst: 'Game'
    clock = pg.time.Clock()
    display: pg.Surface
    editorsTf: list[Transform] = []
    maingameTf: Transform


    def __init__(self, **kwargs):
        Game.inst = self
        Game.display = pg.display.set_mode(Window.native)
        go = Transform('WindowInst', pos=(0, 0), pivot=(0, 0))

        super().__init__(bind=go, **kwargs)
        self.last_display = time.time()
        self.last_frame = time.time()
        self.delta = 0
        self.frame = 0
        self.heldEsc = False


    def windowHandler(self):
        if pgpeek(pg.QUIT):
            Window.running = False
            return
        
        self.try_toggle_devMode()
        self.update_mouse()
        self.update_display()
        self.FPSController()


    def try_toggle_devMode(self):
        if not ALLOW_DEVELOPER or not pgpeek(pg.KEYDOWN): return
        esc = pg.key.get_pressed()[pg.K_ESCAPE]
        if esc and not self.heldEsc:
            self.toggle_devMode()
        self.heldEsc = esc


    def toggle_devMode(self):
        Window.devMode = not Window.devMode
        for editor in Game.editorsTf:
            editor.enabled = Window.devMode

        if Window.devMode:
            Game.maingameTf.scale = vec(0.66, 0.66)
            Game.maingameTf.pos = vec(250, 30)
        else:
            Game.maingameTf.scale = vec(ONE)
            Game.maingameTf.pos = vec(ZERO)
        print(f"Chỉnh chế độ developer sang {Window.devMode}")


    def update_mouse(self):
        host = mouse.host if mouse.host else None # Lỡ bay màu thì hủy
        mouse.pos = vec(pg.mouse.get_pos())
        mouse.clicked = pg.mouse.get_pressed()[0]
        mouse.host = host
        if mouse.lastFocus and mouse.clicked and not mouse.host:
            mouse.lastFocus = None # Click mà không thèm nhận thì thôi


    def update_display(self):
        for pair in Transform.roots.values():
            Game.display.blit(pair[1], pair[0].pos)
            pair[1].fill((0, 0, 0, 0))
        
        pg.display.flip()
        Game.display.fill((0, 0, 0))


    def FPSController(self):
        self.frame += 1
        self.delta = time.time() - self.last_frame
        if time.time() - self.last_display >= 1.0:
            print(f"Possible FPS: {1/self.delta:.2f} | FPS: {self.frame}")
            self.last_display = time.time()
            self.frame = 0
        
        Game.clock.tick(Window.targetFPS)
        self.last_frame = time.time()