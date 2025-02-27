from importer.pg import *
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

_dragging_card = None

def Cardmove(card, event):
    # Hàm xử lý kéo thả card bằng chuột.
    # :param card: Đối tượng card, cần có các thuộc tính:
    #              - pos (Vector2)
    #              - imgsize (Vector2)
    #              - pivot (Vector2)
    #              - dragging (bool)
    #              - offset (Vector2)
    #              và các phương thức:
    #              - is_mouse_inside(mouse)
    #              - on_startClick(), on_stopClick(), on_clicking()
    # :param event: Sự kiện từ Pygame
    global _dragging_card

    if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 1:  # left mouse
            mouse = pg.Vector2(event.pos)
            if card.is_mouse_inside(mouse) and _dragging_card is None:
                _dragging_card = card
                card.dragging = True
                card.offset = card.pos - mouse
                card.on_startClick()

    elif event.type == pg.MOUSEBUTTONUP:
        if event.button == 1 and card.dragging:
            card.dragging = False
            _dragging_card = None
            card.on_stopClick()

    elif event.type == pg.MOUSEMOTION:
        if card.dragging:
            mouse = pg.Vector2(event.pos)
            card.pos = mouse + card.offset
            card.on_clicking()
#  ở đây thì chạy hàm thì m 
# for event in pg.event.get():
#     Cardmove(my_card, event)

