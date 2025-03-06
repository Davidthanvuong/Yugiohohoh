from .header_pygame import *
from typing import Callable, Generic, TypeVar
from weakref import ref as weak

T = TypeVar('T')

class Event(Generic[T]):
    '''Nghe, nhận, thông báo về các event. Dùng cho cập nhật lười'''
    def __init__(self):
        self.listeners: dict[str, tuple[Callable[..., None], GameObject]] = {}

    # Traditional
    def subscribe(self, listener: Callable[..., None]):
        caller = listener.__self__.go # type: ignore
        self.listeners[caller.name] = (listener, caller)

    def unsubscribe(self, listener: Callable[..., None]):
        for key, (lis, cal) in list(self.listeners.items()):
            if lis != listener: continue
            del self.listeners[key]
            return

    def notify(self, arg: No[T] = None):
        not_exist = []
        for key, (lis, cal) in self.listeners.items():
            if cal.exist:
                if arg is not None: lis(arg)
                else: lis()
            else: not_exist.append(key)

        for key in not_exist:
            del self.listeners[key]
            print(f"{key} đã bị xử")


    # Vip pro hiện đại
    def __iadd__(self, listener: Callable[..., None]):
        self.subscribe(listener)
        return self

    def __isub__(self, listener: Callable[..., None]):
        self.unsubscribe(listener)
        return self

    def __imult__(self, arg: T):
        self.notify(arg)
        return self
    
    def __call__(self, arg: No[T] = None):
        self.notify(arg)
        return self