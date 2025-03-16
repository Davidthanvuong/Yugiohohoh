from .engine import *

T = TypeVar('T')
Call = Callable[..., None]

class Event(Generic[T]):
    '''Nghe, nhận, thông báo về các event. Dùng cho cập nhật lười'''

    def __init__(self, initials: No[Call] = None):
        self.listeners: list[weak[Call]] = []
        self.listeners_once: list[weak[Call]] = []

        if initials: self += initials

    def listen(self, listener: Call):
        self.listeners.append(weak(listener))
        return self

    def listen_once(self, listener: Call):
        self.listeners_once.append(weak(listener))
        return self

    def unsubscribe(self, listener: Call):
        self.listeners.remove(weak(listener))
        self.listeners_once.remove(weak(listener))
        return self

    def notify(self, arg: No[T] = None):
        i = 0
        while i < len(self.listeners):
            lis = self.listeners[i]()   # Còn tồn tại không?
            if not lis: 
                self.listeners.pop(i)
                continue

            lis() if arg is None else lis(arg)
            i += 1


    def __iadd__(self, listener: Call):
        return self.listen(listener)

    def __isub__(self, listener: Call):
        return self.unsubscribe(listener)

    def __imul__(self, listener: Call):
        return self.listen_once(listener)
    


class Mouse:
    '''Tốt hơn việc dùng thuần pygame Mouse'''
    pos = vec(1, 0)
    clicked = False
    hoverHost: No[object] = None
    clickHost: No[object] = None
    lastHost : No[object] = None
    dragHost:  No[ref[object]] = None

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

        if cls.dragHost and not cls.dragHost():
            cls.dragHost = None