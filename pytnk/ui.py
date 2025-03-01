from .header_pygame import *

class IClickable(Component):
    '''Click'''
    def __init__(self, hoverable=True, clickable=True, draggable=False, **kwargs):
        super().__init__(**kwargs)

        self.hoverable = hoverable
        self.clickable = clickable
        self.draggable = draggable # Cho phép kéo thả
        self.hovering = False
        self.clicking = False
        self.wasFocus = False

    def try_getMouse(self):
        '''Thử lấy chuột trong hitbox bằng trick xoay'''
        if MOUSE.host and MOUSE.host is not self:
            return False
    
        box = self.tf.hitbox.elementwise() * self.tf.global_scale
        a = box.elementwise() * -self.tf.pivot
        b = a + box

        rel = MOUSE.pos - self.tf.global_pos
        if not self.tf.simple:
            rel.rotate_ip(-self.tf.rot)

        return (a.x <= rel.x <= b.x) and \
               (a.y <= rel.y <= b.y)

    def click_update(self):
        #print(self.hoverable, self.clickable, self.draggable, self.hovering, self.clicking, self.wasFocus)
        if self.try_getMouse():
            if self.hoverable and not self.hovering:
                MOUSE.host = self# Đánh dấu vật đã dùng chuột
                self.hovering = True
                self.on_startHover()
            
            if self.clickable and MOUSE.clicked:
                if not self.clicking:
                    MOUSE.host = self
                    MOUSE.lastFocus = self
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
            MOUSE.host = None
            self.hovering = False

        if self.wasFocus and MOUSE.lastFocus is not self:
            self.on_stopFocus()
            self.wasFocus = False

    # Hàm rỗng nhưng không abstract để cho inheritance
    def logic_update(self): pass
    def on_startHover(self): pass
    def on_startClick(self): pass
    def on_stopHover(self): pass
    def on_stopClick(self): pass
    def on_hovering(self): pass
    def on_clicking(self): pass
    def on_stopFocus(self): pass # là sau khi click vô các object khác



# class ExampleButton(IClickable):
#     '''Nút bấm'''

#     def __init__(self, onClick_phrase: str, spacing: float = 1.2, **kwargs):
#         super().__init__(**kwargs)
#         self.onClick_phrase = onClick_phrase
#         self.spacing = spacing
#         self.texts: list[str] = []
#         self.image = self.tf.get(Image) # Lấy ảnh, không thì báo lỗi :v

#     # Call hàm kiểm click chuột bên trong
        
#     def render_update(self):
#         y = 0
#         for line in self.texts:
#             sf = writer.render(line, True, (0, 0, 0))
#             #direct_render(sf, vec(sf.get_size()), self.tf)
#             dummy_screen.blit(sf, self.tf.pos + vec(0, y))
#             y += self.spacing * FONT_SIZE # Chỉnh font size trong settings.py

#     def on_startClick(self):
#         self.texts.append(self.onClick_phrase)

#     def on_startHover(self):
#         self.tf.scale *= 1.2

#     def on_stopHover(self):
#         self.tf.scale /= 1.2