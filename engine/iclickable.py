from importer.pygame import *
from .transform import Transform
from .abstract_renderer import render
import math

from .abstract_renderer import screen

class IClickable(Transform):
    '''Interface cho tính năng lướt, click, kéo, thả chuột'''
    def __init__(self, clickable=True, draggable=False, **kwargs):
        super().__init__(**kwargs)
        self.clickable = clickable
        self.draggable = draggable  # Cho phép kéo thả
        self.hovering = False
        self.clicking = False

    def rotate_point(self, px, py, cx, cy, angle):
        """ Rotates point (px, py) around (cx, cy) by 'angle' degrees. """
        rad = math.radians(angle)
        sin_a = math.sin(rad)
        cos_a = math.cos(rad)
        
        # Translate point relative to the center
        rel_x, rel_y = px - cx, py - cy
        
        # Apply rotation matrix
        new_x = rel_x * cos_a - rel_y * sin_a + cx
        new_y = rel_x * sin_a + rel_y * cos_a + cy
        return new_x, new_y

    def iclick_update(self):
        '''Cập nhật của interface sẽ kiểm tra chuột hoạt động trên hitbox của host'''
        #todo: Hỗ trợ global và chỉnh kích thước
        mouse_pos = vec(pg.mouse.get_pos())
        isMouseClick = pg.mouse.get_pressed()[0]
        size = self.imgsize

        # Xài lượng giác để tính vị trí của chuột trong tọa độ tương đối của vật
        uv_root = (-self.imgsize.x * self.pivot.x,
                -self.imgsize.y * self.pivot.y)
        angle = self.spin  

        rad = math.radians(-angle)
        cos, sin = math.cos(rad), math.sin(rad)
        rel = mouse_pos - uv_root - self.global_pos()
        rotated_x = rel[0] * cos - rel[1] * sin
        rotated_y = rel[0] * sin + rel[1] * cos
        inside = (0 <= rotated_x <= size.x) and (0 <= rotated_y <= size.y)

        rect_points = [
            self.rotate_point(uv_root[0], uv_root[1], uv_root[0], uv_root[1], angle),
            self.rotate_point(uv_root[0] + size.x, uv_root[1], uv_root[0], uv_root[1], angle),
            self.rotate_point(uv_root[0] + size.x, uv_root[1] + size.y, uv_root[0], uv_root[1], angle),
            self.rotate_point(uv_root[0], uv_root[1] + size.y, uv_root[0], uv_root[1], angle),
        ]
        pg.draw.polygon(screen, (0, 255, 255), rect_points, 2)

        # Draw unrotated bounding box
        pg.draw.rect(screen, (0, 0, 255), (uv_root[0], uv_root[1], size.x, size.y), 1)

        pg.draw.circle(screen, (0, 255, 0) if inside else (255, 0, 0), mouse_pos, 5)        
        pg.draw.circle(screen, (0, 255, 255) if inside else (255, 0, 255), rel, 5)        


        if inside:
            if not self.hovering:
                self.on_startHover()
                self.hovering = True
            
            if self.clickable:
                if isMouseClick:
                    if not self.clicking:
                        self.on_startClick()
                        self.clicking = True
                    self.on_clicking()
                elif self.clicking:
                    self.on_stopClick()
                    self.clicking = False

            self.on_hovering()
        elif self.hovering:
            self.on_stopHover()
            self.hovering = False
            
    # Hàm rỗng nhưng không abstract để cho inheritance
    def on_startHover(self): pass
    def on_startClick(self): pass
    def on_stopHover(self): pass
    def on_stopClick(self): pass
    def on_hovering(self): pass
    def on_clicking(self): pass