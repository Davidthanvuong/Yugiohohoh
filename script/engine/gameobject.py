import pygame as pg
from .settings import *
from .imager import *
from .abstract_renderer import *
from abc import abstractmethod

class GameObject():
    def __init__(self, pos: vec = vec(CENTER)):
        self.pos = pos

    @abstractmethod
    def update(self): pass