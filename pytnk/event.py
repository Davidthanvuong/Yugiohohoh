from .engine import *

T = TypeVar('T')

class Event(Generic[T]):
    '''Nghe, nhận, thông báo về các event. Dùng cho cập nhật lười'''

    def __init__(self):
        self.listeners: dict[Callable[..., None], tuple[weak[Callable[..., None]], bool]] = {}

    def listen(self, listener: Callable[..., None], once: bool = False):
        self.listeners[listener] = (weak(listener), once)

    def listen_once(self, listener: Callable[..., None]):
        self.listen(listener, True)

    def unsubscribe(self, listener: Callable[..., None]):
        self.listeners.pop(listener)

    def notify(self, arg: No[T] = None):
        not_exist = []
        to_remove = []
        old_listeners = self.listeners.items() # Tránh bị lỗi khi tạo vật lúc start
        for key, (weak_lis, once) in list(old_listeners):
            lis = weak_lis()
            if lis:
                if arg is not None:
                    lis(arg)
                else: lis()
                if once: to_remove.append(key)
            else: not_exist.append(key)

        for key in (not_exist + to_remove):
            self.listeners.pop(key)

    def __iadd__(self, listener: Callable[..., None]):
        self.listen(listener)
        return self

    def __isub__(self, listener: Callable[..., None]):
        self.unsubscribe(listener)
        return self

    def __imul__(self, listener: Callable[..., None]):
        self.listen(listener, True)
        return self

    def __call__(self, arg: No[T] = None):
        self.notify(arg)
        return self
    


class Mouse:
    '''Tốt hơn việc dùng thuần pygame Mouse'''
    pos = vec(1, 0)
    clicked = False
    hoverHost: No[object] = None
    clickHost: No[object] = None
    lastHost : No[object] = None
    focusHost: No[ref] = None
    dragHost: No[ref] = None

    @classmethod
    def update_mouse(cls):
        cls.pos = vec(pg.mouse.get_pos())
        cls.clicked = pg.mouse.get_pressed()[0]
        
        # Lưu click host trước đó, dùng cho việc check focus
        if not cls.clicked and cls.clickHost is not None:
            cls.lastHost = cls.clickHost
            cls.clickHost = None

        cls.hoverHost = None # Chuột pygame như gái, thằng nào lấy trước thằng đó thắng
        cls.clickHost = None

        if cls.focusHost and not cls.focusHost():
            cls.focusHost = None

        if cls.dragHost and not cls.dragHost():
            cls.dragHost = None



class Motion:
    def __init__(self, start, stop, duration: float):
        self.t_start = start
        self.t_stop = stop
        self.duration = duration
        self.vector = (self.t_stop - self.t_start) / self.duration

    def start(self):
        self.sinceStart = time()

    def lerp(self):
        delta = time() - self.sinceStart
        return self.start + self.vector * delta
    
    def peak(self):
        return self.t_stop