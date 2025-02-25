from importer.pygame import *
from .transform import Transform
from .abstract_renderer import render
import math

class IClickable():
    '''Interface cho tính năng lướt, click, kéo, thả chuột'''
    def __init__(self, host, clickable=True, draggable=False, **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.clickable = clickable
        self.draggable = draggable  # Cho phép kéo thả
        self.hovering = False

    def iclick_update(self):
        '''Cập nhật của interface sẽ kiểm tra chuột hoạt động trên hitbox của host'''
        #todo: Hỗ trợ global và chỉnh kích thước
        
        mouse = vec(pg.mouse.get_pos())
        size = self.host.imgsize

        # Xài lượng giác để tính vị trí của chuột trong tọa độ tương đối của vật
        rect = (self.host.pos.x - self.host.imgsize.x * self.host.pivot.x,
                self.host.pos.y - self.host.imgsize.y * self.host.pivot.y)
        angle = self.host.spin  

        rad = math.radians(-angle)
        cos, sin = math.cos(rad), math.sin(rad)
        rel = mouse - rect
        rotated_x = rel[0] * cos - rel[1] * sin
        rotated_y = rel[0] * sin + rel[1] * cos
        inside = (0 <= rotated_x <= size.x) and (0 <= rotated_y <= size.y)

        if inside:
            if not self.hovering:
                self.host.on_startHover()
                self.hovering = True
            self.host.on_hovering()
        else:
            if self.hovering:
                self.host.on_stopHover()
                self.hovering = False
            
    # Hàm rỗng nhưng không abstract để cho inheritance
    def on_startHover(self): pass
    def on_startClick(self): pass
    def on_stopHover(self): pass
    def on_stopClick(self): pass
    def on_hovering(self): pass
    def on_clicking(self): pass