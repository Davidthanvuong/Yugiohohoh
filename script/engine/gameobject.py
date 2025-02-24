from .settings import *
from typing import Optional
from abc import abstractmethod
import pygame as pg

class GameObject():
    

    def __init__(self, pos: vec = vec(0, 0), scale = vec(1, 1), post_scale = vec(1, 1), 
                 spin = 0.0, pivot = vec(0.5, 0.5), hitbox = vec(100, 100), parent: Optional['GameObject'] = None):
        self.pos = pos
        self.scale = scale
        self.post_scale = post_scale
        self.spin = spin
        self.pivot = pivot
        self.parent = parent
        self.hitbox = hitbox

        self.clickable = False

    @abstractmethod
    def update(self):
        '''Nhớ super() sau cùng chứ không phải đầu tiên nha'''

        if self.clickable:
            pos = pg.mouse.get_pos()
            # todo: Rect with rotate??
            hovered = False
            if hovered:
                self.onHover()
                if pg.mouse.get_pressed():
                    self.onClick()



    @abstractmethod
    def onHover(self): pass

    @abstractmethod
    def onClick(self): pass

    @abstractmethod
    def onDebug(self): pass