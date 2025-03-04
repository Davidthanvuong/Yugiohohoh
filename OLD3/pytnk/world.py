from .header_pygame import *
from .abstract_renderer import updateDisplay
import pickle, os, time

class World(Component):
    '''Za warudo! :insert_ngưng_động_thời_gian: :penguin:'''
    inst: 'World'
    RUNNING = True
    clock = pg.time.Clock()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        World.inst = self
        self.last_display = time.time()
        self.last_frame = time.time()
        self.delta = 0
        self.frame = 0
        self.esc_ed = False
        self.tf.pos = vec(0, 0) # Tạo object world mặt định phải góc trái trên
        self.tf.pivot = vec(0, 0)
        # self.com_image = self.tf.get(Image)
        # self.com_image.cache.native.fill(colormap['dark'])


    def windowHandler(self):
        '''Cập nhật trạng thái chuột, giữ ổn định FPS đồng thời kiểm có tắt app ko'''
        global RUNNING, DEVELOPER, MOUSE

        if pgpeek(pg.QUIT):
            World.RUNNING = False
            return
        
        if ALLOW_DEVELOPER and pgpeek(pg.KEYDOWN):
            esc = pg.key.get_pressed()[pg.K_ESCAPE]
            if esc and not self.esc_ed:
                DEVELOPER = not DEVELOPER
                if DEVELOPER:
                    self.tf.scale = vec(0.66, 0.66)
                    self.tf.pos = vec(250, 30)
                    Editor.inst.tf.enable = True
                else:
                    self.tf.scale = vec(ONE)
                    self.tf.pos = vec(0, 0)
                    Editor.inst.tf.enable = False
                print(f"Chỉnh chế độ developer sang {DEVELOPER}")
            self.esc_ed = esc

        host = MOUSE.host if MOUSE.host else None # Lỡ bay màu thì hủy
        MOUSE.pos = vec(pg.mouse.get_pos())
        MOUSE.clicked = pg.mouse.get_pressed()[0]
        MOUSE.host = host
        if MOUSE.lastFocus and MOUSE.clicked and not MOUSE.host:
            MOUSE.lastFocus = None # Click mà không thèm nhận thì thôi

        updateDisplay()
        self.frame += 1
        self.delta = time.time() - self.last_frame
        if time.time() - self.last_display >= 1.0:
            print(f"Possible FPS: {1/self.delta:.2f} | FPS: {self.frame}")
            self.last_display = time.time()
            self.frame = 0
        
        World.clock.tick(TARGET_FPS)
        self.last_frame = time.time()