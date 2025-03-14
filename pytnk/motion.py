from .engine import *
from typing import Any
# pyright: reportArgumentType=false

class Motion:
    def __init__(self, func: Callable[[float], float], begin, dest, duration: float, repeat = False, wave = False):
        self.func = func
        self.begin = begin
        self.dest = dest
        self.duration = duration
        self.repeat = repeat
        self.wave = wave
        self.vector = self.dest - self.begin
        self.start()

    def start(self):
        self.sinceStart = now()
    
    @property
    def value(self):
        t = (now() - self.sinceStart) / self.duration
        if self.repeat: 
            t = 1 - abs((t % 2) - 1) if self.wave else t % 1
        self.t = t
        return self.begin + self.vector * self.func(t)

    @property
    def completed(self): # repeat bật vẫn kêu, coi như là chu kì
        return now() - self.sinceStart >= self.duration
    
    def sleep(*a: Any):                 return Motion(lambda t: t, 0, 1, *a)
    def linear(*a: Any):                return Motion(lambda t: t, *a)
    def ease_out(*a: Any):              return Motion(lambda t: 1 - math.sin(t * DEGREE90), *a)
    def ease_in(*a: Any):               return Motion(lambda t: 1 - math.cos(t * DEGREE90), *a)
    def ease_out_cubic(*a: Any):        return Motion(lambda t: 1 - (1 - math.sin(t * DEGREE90)) ** 3, *a)