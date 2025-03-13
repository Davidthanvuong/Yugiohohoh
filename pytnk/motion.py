from .engine import *
from typing import Any
# pyright: reportArgumentType=false

class Motion:
    def __init__(self, func: Callable[[float], float], begin, dest, duration: float, delay = 0.0):
        self.func = func
        self.begin = begin
        self.dest = dest
        self.duration = duration
        self.delay = delay
        self.vector = self.dest - self.begin
        self.t = 0.0
        self.start()

    def start(self):
        self.sinceStart = now() + self.delay
    
    @property
    def value(self):
        t = (now() - self.sinceStart) / self.duration
        self.t = max(0, min(1, t))
        return self.begin + self.vector * self.func(self.t)

    @property
    def completed(self):
        return now() - self.sinceStart >= self.duration
    
    def sleep(*a: Any):                 return Motion(lambda t: t, 0, 1, *a)
    def linear(*a: Any):                return Motion(lambda t: t, *a)
    def ease_out(*a: Any):              return Motion(lambda t: 1 - math.sin(t * DEGREE90), *a)
    def ease_in(*a: Any):               return Motion(lambda t: 1 - math.cos(t * DEGREE90), *a)
    def ease_out_cubic(*a: Any):        return Motion(lambda t: 1 - (1 - math.sin(t * DEGREE90)) ** 3, *a)