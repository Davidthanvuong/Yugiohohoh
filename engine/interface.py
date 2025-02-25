from importer.pygame import *
from .transform import Transform
import math
from .abstract_renderer import render

class IClickable():
    '''Interface cho tính năng lướt, click, kéo, thả chuột'''
    def __init__(self, host, clickable=True, draggable=False, **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.clickable = clickable
        self.draggable = draggable  # Cho phép kéo thả
        self.white = Transform(
            imgpath="white.png", 
            imgsize=self.host.imgsize,
            parent=self.host, 
            pivot=self.host.pivot
        )
        self.hovering = False

    def rotate_point(px, py, cx, cy, angle):
        rad = math.radians(angle)
        sin_a = math.sin(rad)
        cos_a = math.cos(rad)
        rel_x, rel_y = px - cx, py - cy
        new_x = rel_x * cos_a - rel_y * sin_a + cx
        new_y = rel_x * sin_a + rel_y * cos_a + cy
        return new_x, new_y

    def is_mouse_in_rotated_rect(mouse_x, mouse_y, rect_x, rect_y, width, height, angle):
        """
        """
        rad = math.radians(-angle)
        rel_x = mouse_x - rect_x
        rel_y = mouse_y - rect_y
        rotated_x = rel_x * math.cos(rad) - rel_y * math.sin(rad)
        rotated_y = rel_x * math.sin(rad) + rel_y * math.cos(rad)
        inside = (0 <= rotated_x <= width) and (0 <= rotated_y <= height)
        return inside, rotated_x, rotated_y

    def iclick_update(self):
        '''Cập nhật của interface sẽ kiểm tra chuột hoạt động trên hitbox của host'''
        render(self.white)  
        
        mouse_x, mouse_y = pg.mouse.get_pos()
        
        rect_x = self.host.pos.x - self.host.imgsize.x * self.host.pivot.x
        rect_y = self.host.pos.y - self.host.imgsize.y * self.host.pivot.y
        rect_width = self.host.imgsize.x
        rect_height = self.host.imgsize.y
        angle = self.host.spin  

        inside, rotated_mouse_x, rotated_mouse_y = IClickable.is_mouse_in_rotated_rect(
            mouse_x, mouse_y,
            rect_x, rect_y,
            rect_width, rect_height,
            angle
        )

        if inside:
            if not getattr(self, 'hovering', False):
                self.host.on_startHover()
            self.hovering = True
            # self.host.on_hovering()
        else:
            self.hovering = False
            
    
    def on_startHover(self): pass

    
    def on_startClick(self): pass
    
    
    def on_stopHover(self): pass
    
    
    def on_stoClick(self): pass
    
    
    def on_hovering(self): pass
    
    
    def on_clicking(self): pass