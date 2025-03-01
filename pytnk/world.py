from .header_pygame import *
from .abstract_renderer import updateDisplay
import pickle, os

class World(Component):
    RUNNING = True
    clock = pg.time.Clock()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tf.pos = vec(0, 0)
        self.tf.pivot = vec(0, 0)
        self.esc_ed = False
        if ALLOW_DEVELOPER:
            self.tool = Transform(parent=self.tf, enable=False)
            Image("card_back.png", attach=self.tool)

    def windowHandler(self):
        '''Cập nhật trạng thái chuột và kiểm có tắt ko'''
        global RUNNING, DEVELOPER, MOUSE
        if pgpeek(pg.QUIT):
            World.RUNNING = False
            return
        
        #print(self.esc_ed)
        if ALLOW_DEVELOPER and pgpeek(pg.KEYDOWN):
            esc = pg.key.get_pressed()[pg.K_ESCAPE]
            if esc and not self.esc_ed:
                DEVELOPER = not DEVELOPER
                self.tool.enable = DEVELOPER
                print(f"Toggled to {DEVELOPER}")
            self.esc_ed = esc

        host = MOUSE.host if MOUSE.host else None # Lỡ bay màu thì hủy
        MOUSE.pos = vec(pg.mouse.get_pos())
        MOUSE.clicked = pg.mouse.get_pressed()[0]
        MOUSE.host = host
        if MOUSE.lastFocus and MOUSE.clicked and not MOUSE.host:
            MOUSE.lastFocus = None # Click mà không thèm nhận thì thôi

        updateDisplay()
        World.clock.tick(TARGET_FPS)

    # active: dict[str, 'Scene'] = {}

    # def __init__(self, name: str, load: bool = False):
    #     self.name = name
    #     Scene.active[name] = self
    #     if load:
    #         full = f"{Scene.folder}{name}"
    #         if os.path.exists(full):
    #             with open(full, "rb") as f:
    #                 self.objects = pickle.load(f)
    #             print(f"Load success {full}")

    #         print(f"No file {full} existed")
    #         raise Exception(f"Không có file")
    #     else:
    #         self.objects: dict[str, Transform] = {}

    # def add(self, tf: Transform) -> Transform:
    #     self.objects[tf.name] = tf
    #     return tf

    # def update(self, renderOnly = False):
    #     '''Cập nhật Scene theo trình tự logic --> render'''
    #     if not renderOnly:
    #         for obj in self.objects.values():
    #             obj.logic_update()

    #         for obj in reversed(self.objects.values()):
    #             obj.click_update()

    #     for obj in self.objects.values():
    #         obj.render_update()


    # @staticmethod
    # def update_all():
    #     for scene in Scene.active.values():
    #         scene.update()