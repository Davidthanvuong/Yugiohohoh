from importer.gobj import *
from .abstract_renderer import RENDER
from time import time as get_time

class FPSCounter(Transform):
    def __init__(self):
        self.last_time = get_time()
        self.frame = 0
        self.textr = Textr()
        self.fps_text = ""

    def update(self):
        self.frame += 1
        curr = get_time()
        if curr - self.last_time >= 0.5:
            dt = (curr - self.last_time)
            fps = self.frame / dt
            mspf = 1000 / fps
            self.fps_text = f"FPS: {int(fps)}\nMSPF: {mspf:.2f} ms\nRendering on: {RENDER.name}"
            self.last_time = curr
            self.frame = 0
        
        self.textr.write(self.fps_text, vec(0, 0))