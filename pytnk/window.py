from .header_pygame import *
from time import time


class Scene:
    '''Object đơn giản dùng để render khung màn hình'''

    def __init__(self, go: 'GameObject', sf: pg.Surface):
        self.go = go
        self.buffer = sf
        self.gizmos: list[tuple[RGB, tff, tff, int]] = []

    def gizmos_rect(self, color: RGB, scope: 'Scope | tuple[tff, tff]', inset: int = 1):
        '''Lưu gizmos là các renderbox để render trên cùng'''
        #Không thể tạo nếu scope chưa được render (tự đánh dấu r)
        #Nhưng chắc chắn có rect thì chạy được
        if isinstance(scope, Scope):
            if not scope.valid: return
            topleft, size = scope.convert()
            self.gizmos.append((color, topleft, size, inset))
        else:
            self.gizmos.append((color, scope[0], scope[1], inset))


class Window:
    '''Za warudo! :insert_ngưng_động_thời_gian: :penguin:'''
    Display: pg.Surface
    Scenes: dict[str, Scene] = {}
    EditorsName: list[str] = []
    # Tên: Gốc vật, surface render riêng, developer?

    e_onDisplayChange: Event = Event()
    running = True
    targetFPS = 999
    fpsTrackDur = 5.0
    useOpenGL = False
    defRatio = 900 / 500
    defNative = (900, 500)
    native = (900, 500)
    vNative = vec(native)
    devMode = False
    clock = pg.time.Clock()


    def __init__(self):
        self.last_display = time()
        self.last_frame = time()
        self.frameDuration = 0
        self.totalFrame = 0
        self.logic_time = 0.0
        self.click_time = 0.0
        self.render_time = 0.0
        self.upload_time = 0.0
        self.heldEsc = False
        self.mainGame = None


    def __call__(self, text: str) -> 'Window':
        print(f"Started with parameters {text}")
        pg.init()
        Window.Display = pg.display.set_mode(Window.native, pg.RESIZABLE)
        return self


    def inputHandle(self):
        if pgpeek(pg.QUIT):
            Window.running = False
            return

        if pgpeek(pg.VIDEORESIZE):
            self.handle_windowResize()

        self.try_toggle_devMode()
        self.update_mouse()    


    def mainLoop(self):
        t = time()
        for scene in Window.Scenes.values():
            scene.go.update_logic()

        self.logic_time += time() - t
        
        t = time()
        for scene in reversed(Window.Scenes.values()):
            scene.go.update_click()

        self.click_time += time() - t

        t = time()
        for scene in Window.Scenes.values():
            scene.go.update_render()

        self.render_time += time() - t


    def outputHandle(self):
        t = time()
        self.updateDisplay()
        self.upload_time += time() - t

        self.trackFPS()
        
        
    def updateDisplay(self):
        for root in Window.Scenes.values():
            Window.Display.blit(root.buffer, root.go.global_pos)
            root.buffer.fill((0, 0, 0, 0))

            # Gizmos vẽ sau blit
            for color, topleft, size, width in root.gizmos:
                rect = pg.Rect(topleft + root.go.global_pos, size)
                if width < 0: 
                    rect = rect.inflate(-width * 2, -width * 2) # Nếu âm thì extrude (inflate) thay vì inset
                pg.draw.rect(Window.Display, color, rect, abs(width))

            root.gizmos.clear()
        
        pg.display.update()
        Window.Display.fill(Color.black)
        

    def trackFPS(self):
        self.totalFrame += 1
        self.frameDuration += time() - self.last_frame
        dt = time() - self.last_display

        if dt >= Window.fpsTrackDur:
            pfr = 1000 / self.totalFrame
            str_fps = f"{self.totalFrame / Window.fpsTrackDur} FPS"
            str_latency = f"(CPU ~{self.frameDuration:.2f}/{Window.fpsTrackDur}s)"
            str_work = f"{self.logic_time * pfr:.2f} -> {self.click_time * pfr:.2f}"
            str_graphic = f"-> {self.render_time * pfr:.2f} -> {self.upload_time * pfr:.2f} (ms/frame)"
            print(f"| {str_fps} {str_latency}\n| {str_work} {str_graphic}")
            self.last_display = time()
            self.totalFrame = 0
            self.frameDuration = 0.0
            self.logic_time = 0.0
            self.click_time = 0.0
            self.render_time = 0.0
            self.upload_time = 0.0
        
        Window.clock.tick(Window.targetFPS)
        self.last_frame = time()


    def handle_windowResize(self):
        for event in pg.event.get(pg.VIDEORESIZE):
            Window.native = event.w, event.h
            Window.vNative = vec(Window.native)
            Window.Display = pg.display.set_mode(Window.native, pg.RESIZABLE)
            Window.e_onDisplayChange.notify()


    def try_toggle_devMode(self):
        if not ALLOW_DEVELOPER or not pgpeek(pg.KEYDOWN): return
        esc = pg.key.get_pressed()[pg.K_ESCAPE]
        if esc and not self.heldEsc:
            self.toggle_devMode()
        self.heldEsc = esc


    def toggle_devMode(self):
        Window.devMode = not Window.devMode
        for root in Window.Scenes.values(): # O(N^2) :))
            if root.go.name in Window.EditorsName: 
                root.go.enabled = Window.devMode

        Window.e_onDisplayChange.notify()
            
        print(f"Chỉnh chế độ developer sang {Window.devMode}")


    def update_mouse(self):
        Mouse.pos = vec(pg.mouse.get_pos())
        Mouse.clicked = pg.mouse.get_pressed()[0] 
        Mouse.hover = None # Tự reset lại, thằng nào chiếm trước thằng đó thắng
        if (not Mouse.clicked):
            Mouse.lastClick = Mouse.click
            Mouse.click = None # Nếu ngưng click mới lưu
        if (Mouse.lastClick != Mouse.focus):
            Mouse.focus = None # Hoặc bị bay màu hoặc click sang vật khác


class Scope:
    '''Phạm vi render của một vật hoặc một cây'''
    def __init__(self):
        self.update(None) # Khởi tạo

    def convert(self):
        return (self.left, self.top), (self.right - self.left, self.top - self.bottom)


    def update(self, other: 'pg.Rect | Scope | None') -> 'Scope':
        self.valid = True
        if isinstance(other, Scope):
            self.left   = min(self.left,    other.left)
            self.top    = min(self.top,     other.top)
            self.right  = max(self.right,   other.right)
            self.bottom = max(self.bottom,  other.bottom)
        elif isinstance(other, pg.Rect):
            self.left   = min(self.left,    other.left)
            self.top    = min(self.top,     other.top)
            self.right  = max(self.right,   other.right)
            self.bottom = max(self.bottom,  other.bottom)
        else:
            self.valid = False
            self.left   = Window.native[0]
            self.top    = Window.native[1]
            self.right  = 0
            self.bottom = 0
        return self