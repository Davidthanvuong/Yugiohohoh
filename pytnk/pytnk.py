from .engine import *

class Pytnk:
    clock = pg.time.Clock()
    heldEsc = False

    @classmethod
    def start(cls):
        '''Bắt đầu pygame như bth thôi'''
        pg.init()
        App.screen = pg.display.set_mode(App.native)
        pg.display.set_caption("PyTNK @ Yugiohohoh (09/03)")
        App.gameStarted = True
        root = GameObject('Root')

        # root.restart()

        # Sequence.e_finished += cls.sequenceHandler
        #cls.root += FPSCounter()

    # @classmethod
    # def start(cls):
    #     '''Bắt đầu game'''
    #     # Component.e_notStarted.notify()

    @classmethod
    def update(cls):
        if cls.input_handler(): return
        GameObject.root.update_logic()
        GameObject.root.update_click()
        GameObject.root.update_render()
        pg.display.update()
        App.screen.fill(Color.black)

        cls.clock.tick(App.targetFPS)

    @classmethod
    def input_handler(cls):
        if pgpeek(pg.QUIT):
            App.running = False
            return True

        cls.try_toggleDev()
        Mouse.update_mouse()

    # @classmethod
    # def sequenceHandler(cls, seq: Sequence):
    #     if isinstance(seq, IntroSeq): 
    #         cls.load_loadingScreen()

    #     elif isinstance(seq, LoadingSeq): 
    #         cls.load_maingame()

    @classmethod
    def try_toggleDev(cls):
        if not ALLOW_DEVELOPER or not pgpeek(pg.KEYDOWN): return
        esc = pg.key.get_pressed()[pg.K_ESCAPE]
        canToggle = esc and not cls.heldEsc
        cls.heldEsc = esc
        if not canToggle: return

        App.devMode = not App.devMode
        if App.devMode:
            pg.display.set_mode(App.devNative)
        else:
            pg.display.set_mode(App.native)

    

    @classmethod
    def load_intro(cls):
        GameObject.loadPrefab("Intro Scene")

    @classmethod
    def load_loadingScreen(cls):
        GameObject.loadPrefab("Loading Scene")

    @classmethod
    def load_maingame(cls):
        GameObject.loadPrefab("Maingame Scene")