from ..engine.gameobject import *
from time import time as get_time

class FPSCounter(GameObject):
    def __init__(self):
        self.last_time = get_time()
        self.frame = 0
        self.fps_text = ""

    def update(self):
        self.frame += 1
        curr = get_time()
        if curr - self.last_time >= 0.5:
            fps = self.frame / (curr - self.last_time)
            self.fps_text = f"FPS: {fps:.2f}"
            self.last_time = curr
            self.frame = 0
        
        write(self.fps_text, vec(0, 0))