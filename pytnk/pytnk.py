from .engine import *

class Pytnk:
    root: 'GameObject'
    clock = pg.time.Clock()
    heldEsc = False

    @classmethod
    def init(cls):
        '''Bắt đầu pygame như bth thôi'''
        pg.init()
        App.display = pg.display.set_mode(App.native)
        pg.display.set_caption("PyTNK @ Yugiohohoh (09/03)")
        GameObject.defaultParent = cls.root = GameObject('Root')

        Sequence.e_finished += cls.sequenceHandler
        #cls.root += FPSCounter()

    @classmethod
    def start(cls):
        '''Bắt đầu game'''
        App.gameStarted = True
        Component.e_notStarted.notify()

    @classmethod
    def update(cls):
        if cls.input_handler(): return
        cls.event_handler()
        cls.root.update_logic()
        cls.root.update_click()
        cls.root.update_render()
        pg.display.update()
        App.display.fill(Color.black)

        cls.clock.tick(App.targetFPS)

    @classmethod
    def input_handler(cls):
        if pgpeek(pg.QUIT):
            App.running = False
            return False

        cls.try_toggleDev()
        Mouse.update_mouse()
        
    @classmethod
    def event_handler(cls):
        pass#

    @classmethod
    def sequenceHandler(cls, seq: Sequence):
        if isinstance(seq, IntroSeq): 
            cls.load_loadingScreen()

        elif isinstance(seq, LoadingSeq): 
            cls.load_maingame()

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