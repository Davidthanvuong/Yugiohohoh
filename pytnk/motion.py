from .engine import *
from typing import Any
# pyright: reportArgumentType=false

class Motion:
    actives: dict['Motion', tuple[ref, str]] = {}
    speed = 1.0
    lastFrame = now()
    dt = 0.0

    @classmethod
    def update_all(cls):
        cls.dt = (now() - cls.lastFrame) * cls.speed
        cls.lastFrame = now()
        for motion, (target, attr) in list(Motion.actives.items()):
            obj = target()
            if obj is None:
                del cls.actives[motion]
                continue

            if motion.completed:
                setattr(obj, attr, motion.dest)
                if motion.onFinish:
                    motion.onFinish()
                del cls.actives[motion]
            else:
                setattr(obj, attr, motion.value)

    def __init__(self, func: Callable[[float], float], begin, dest, duration: float, repeat = False, wave = False):
        self.func = func
        self.begin = begin
        self.dest = dest
        self.speed = 1 / duration
        self.repeat = repeat
        self.wave = wave
        self.vector = self.dest - self.begin
        self.lastFrame = now()
        self.willComplete = False
        self.onFinish: No[Callable] = None
        self.start()

    def start(self):
        self.lifetime = 0.0
    
    def bind(self, target, attr: str, onFinish: No[Callable] = None):
        Motion.actives[self] = (ref(target), attr)
        self.onFinish = onFinish
        return self

    def unbind(self):
        Motion.actives.pop(self)

    def update_lifetime(self):
        if self.lastFrame != Motion.lastFrame:
            self.lastFrame = Motion.lastFrame
            self.lifetime += Motion.dt * self.speed
            if self.lifetime >= 1: 
                self.willComplete = True
            return True
        return False

    @property
    def value(self):
        if self.update_lifetime(): # Cập nhật lười có kiểm
            t = self.lifetime
            if self.repeat: t = 1 - abs((t % 2) - 1) if self.wave else t % 1
            elif self.wave: t = 1 - abs(t * 2 - 1)
        else: t = self.lifetime
        return self.begin + self.vector * self.func(min(t, 1))

    @property
    def completed(self): # repeat bật vẫn kêu, coi như là chu kì
        self.update_lifetime()
        return (self.willComplete) and (self.lifetime >= 1)
    
    def sleep(*a: Any):                 return Motion(lambda t: t, 0, 1, *a)
    def linear(*a: Any):                return Motion(lambda t: t, *a)
    def ease_in(*a: Any):               return Motion(lambda t: 1 - math.cos(t * HALF_RADIAN), *a)
    def ease_in_cubic(*a: Any):         return Motion(lambda t: 1 - (math.cos(t * HALF_RADIAN)) ** 3, *a)
    def ease_out(*a: Any):              return Motion(lambda t: math.sin(t * HALF_RADIAN), *a)
    def ease_out_cubic(*a: Any):        return Motion(lambda t: 1 - (1 - math.sin(t * HALF_RADIAN)) ** 3, *a)
    def quadratic_in(*a: Any):          return Motion(lambda t: 1 - (1 - t) ** 2, *a)