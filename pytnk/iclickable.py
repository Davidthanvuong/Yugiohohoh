from .header_pygame import *

class IClickable(Component):
    '''Hỗ trợ click'''

    def __init__(self, hoverable=True, clickable=True, draggable=False, **kwargs):
        super().__init__(**kwargs)

        self.hoverable = hoverable
        self.clickable = clickable
        self.draggable = draggable # todo: Cho phép kéo thả (builtin)

        self.hovering = False
        self.clicking = False
        self.wasFocus = False
        self.clickDelta = vec(ZERO)


    def is_mouseInHitbox(self):
        '''Thử lấy chuột trong hitbox bằng trick xoay'''
        box = self.go.hitbox.elementwise() * self.go.global_scale
        a = box.elementwise() * -self.go.pivot
        b = a + box

        rel = Mouse.pos - self.go.global_pos
        if not self.go.simple:
            rel.rotate_ip(-self.go.rot)

        return (a.x <= rel.x <= b.x) and \
               (a.y <= rel.y <= b.y)


    def update_click(self):
        #print(self.hoverable, self.clickable, self.draggable, self.hovering, self.clicking, self.wasFocus)
        canFocus = (not Mouse.click) or (Mouse.click is self)
        if self.hoverable and self.is_mouseInHitbox() and canFocus:
            if not self.hovering and not Mouse.hover: # Nếu đang hover và chưa bị lấylấy
                Mouse.hover = self # Đánh dấu vật đã dùng chuột
                self.hovering = True
                self.on_startHover()
            
            if self.clickable and Mouse.clicked: # Đã kiểm click hay chưa trong try_getMouse
                if not self.clicking:
                    Mouse.click = self
                    Mouse.focus = self
                    self.clicking = True
                    self.wasFocus = True
                    self.on_startClick()
                    if self.draggable:
                        self.on_startDrag()

                self.on_clicking()
                if self.draggable:
                    self.on_dragging()

            elif self.clicking:
                self.clicking = False
                self.on_stopClick()

            self.on_hovering()
            
        elif self.hovering:
            self.on_stopHover()
            # x Mouse.hover = None | Chuột đã bị lấy, đừng reset Mouse.hover
            self.hovering = False

        if (self.wasFocus) and not (Mouse.focus is self):
            # Lúc tập trung, ngưng khi không phải bản thân 
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

    def on_startDrag(self):
        self.clickDelta = Mouse.pos.elementwise() * self.go.scene.go.global_scale + self.go.scene.go.global_pos

    def on_dragging(self):
        self.go.pos = Mouse.pos.elementwise() * self.go.scene.go.global_scale - self.go.scene.go.global_pos + self.clickDelta