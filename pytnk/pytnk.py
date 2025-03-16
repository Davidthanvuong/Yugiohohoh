from .engine import *

class Pytnk:
    clock = pg.time.Clock()

    @classmethod
    def start(cls):
        '''Bắt đầu pygame như bth thôi'''
        pg.init()
        # pg.mixer.init()
        App.screen = pg.display.set_mode(App.native)
        pg.display.set_caption("PyTNK @ Yugiohohoh (09/03)")
        GameObject('Root')

    @classmethod
    def update(cls):
        if pgpeek(pg.QUIT):
            App.running = False
            return True

        Mouse.update_mouse()
        Motion.update_all()
        GameObject.root.update_logic()
        GameObject.root.update_click()
        GameObject.root.update_render()
        pg.display.update()
        App.screen.fill(Color.black)

        cls.clock.tick(App.targetFPS)        