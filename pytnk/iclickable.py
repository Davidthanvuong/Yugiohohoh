from .header_pygame import *

class IClickable(Component):
    '''Click quốc dân'''

    def __init__(self, hoverable=True, clickable=True, draggable=False, **kwargs):
        super().__init__(**kwargs)

        self.hoverable = hoverable
        self.clickable = clickable
        self.draggable = draggable # todo: Cho phép kéo thả
        self.hovering = False
        self.clicking = False
        self.wasFocus = False


    def try_getMouse(self):
        '''Thử lấy chuột trong hitbox bằng trick xoay'''
        if mouse.host and mouse.host is not self:
            return False
    
        box = self.tf.hitbox.elementwise() * self.tf.global_scale
        a = box.elementwise() * -self.tf.pivot
        b = a + box

        rel = mouse.pos - self.tf.global_pos
        if not self.tf.no_angle:
            rel.rotate_ip(-self.tf.angle)

        return (a.x <= rel.x <= b.x) and \
               (a.y <= rel.y <= b.y)


    def update_click(self):
        #print(self.hoverable, self.clickable, self.draggable, self.hovering, self.clicking, self.wasFocus)
        if self.hoverable and self.try_getMouse():
            if not self.hovering:
                mouse.host = self # Đánh dấu vật đã dùng chuột
                self.hovering = True
                self.on_startHover()
            
            if self.clickable and mouse.clicked:
                if not self.clicking:
                    mouse.host = self
                    mouse.lastFocus = self
                    self.clicking = True
                    self.wasFocus = self
                    self.on_startClick()
                self.on_clicking()
            elif self.clicking:
                self.clicking = False
                self.on_stopClick()

            self.on_hovering()
        elif self.hovering:
            self.on_stopHover()
            mouse.host = None
            self.hovering = False

        if self.wasFocus and mouse.lastFocus is not self:
            self.on_stopFocus()
            self.wasFocus = False


    # Hàm rỗng nhưng không abstract để cho inheritance
    def on_startHover(self): pass
    def on_startClick(self): pass
    def on_stopHover(self): pass
    def on_stopClick(self): pass
    def on_hovering(self): pass
    def on_clicking(self): pass
    def on_stopFocus(self): pass # là sau khi click vô các object khác