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
        
        DamagePooling.init()

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
        DamagePooling.update_pool()

        if App.blackwhiteFilter:
            bw_surface = pg.Surface(App.screen.get_size())
            bw_surface.blit(App.screen, (0, 0))
            pg.transform.threshold(bw_surface, bw_surface, (0, 0, 0), (100, 100, 100), (200, 0, 0), 1)
            App.screen.blit(bw_surface, ZERO)

        pg.display.update()
        App.screen.fill(Color.black)

        cls.clock.tick(App.targetFPS)        