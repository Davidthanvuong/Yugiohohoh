from .settings import *
from typing import Optional
from abc import abstractmethod

class GameObject():
    def __init__(self, pos: vec = vec(0, 0), scale = vec(1, 1), post_scale = vec(1, 1), 
                 spin = 0.0, pivot = vec(0.5, 0.5), parent: Optional['GameObject'] = None):
        self.pos = pos
        self.scale = scale
        self.post_scale = post_scale
        self.spin = spin
        self.pivot = pivot
        self.parent = parent

    @abstractmethod
    def update(self): pass