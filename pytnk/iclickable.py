from .engine import *

class IClickable(Component):
    '''Base class cho việc xử lí chuột'''
    def __init__(self, hoverable=True, clickable=True, draggable=False):
        self.hoverable = hoverable
        self.clickable = clickable
        self.draggable = draggable

        self.hovering = False
        self.clicking = False
        self.dragging = False
        self.wasFocus = False
        self.clickDelta = vec(0, 0)

    def is_mouseInHitbox(self):
        '''Thử lấy chuột trong hitbox bằng trick xoay'''
        size = self.transf.l_hitboxSize
        topleft = size.elementwise() * (- self.transf.anchor)
        bottomright = topleft + size

        rel = Mouse.pos - self.transf.g_pos
        if not self.transf.straight:
            rel.rotate_ip(-self.transf.rot)

        #print(topleft.x, rel.x, bottomright.x, "and", topleft.y, rel.y, bottomright.y)
        return (topleft.x <= rel.x <= bottomright.x) and \
               (topleft.y <= rel.y <= bottomright.y)

    def update_click(self):
        # Hover None lúc đầu, thằng nào lấy trước thằng đó thắng
        inHitbox = self.is_mouseInHitbox()
        canHover = self.hoverable and inHitbox and (Mouse.dragHost or not Mouse.hoverHost)
        if canHover:
            if not self.hovering:
                self.hovering = True
                self.on_startHover()
            Mouse.hoverHost = self
            self.on_hovering()
        elif self.hovering:
            self.hovering = False
            self.on_stopHover()

        # Thập cẩm: Click, drag, focus
        # Đây là code sỏi thận sỏi mật
        canClick = self.dragging or (self.clickable and not Mouse.clickHost and inHitbox)
        if canClick and Mouse.clicked:
            if not self.clicking:
                self.clicking = True
                self.wasFocus = True
                Mouse.focusHost = ref(self)
                self.on_startClick()
                if self.draggable:
                    self.dragging = True
                    Mouse.dragHost = ref(self)
                    self.on_startDrag()
            Mouse.clickHost = self
            self.on_clicking()
            if self.draggable:
                self.on_dragging()
        elif self.clicking:
            self.clicking = False
            self.on_stopClick()
            if self.dragging:
                self.dragging = False
                Mouse.dragHost = None
                self.on_stopDrag()

        if self.wasFocus and not self.clicking and Mouse.lastHost is not self:
            self.wasFocus = False
            self.on_stopFocus()
        
        # if canClick and Mouse.clicked:
        #     Mouse.clickHost = ref(self.go)
        #     Mouse.focusHost = Mouse.clickHost

        # if Mouse.clickHost and Mouse.clickHost() == self.go:
        #     if not self.clicking:
        #         self.clicking = True
        #         self.on_startClick()
        #         if self.draggable:
        #             self.on_startDrag()
        #     self.on_clicking()
        #     if self.draggable:
        #         self.on_dragging()
        # else:
        #     if self.clicking:
        #         self.clicking = False
        #         self.on_stopClick()

        # # Focus logic: Retain focus until another object is clicked
        # prev_wasFocus = self.wasFocus
        # self.wasFocus = (Mouse.focusHost and Mouse.focusHost() == self.go)
        # if prev_wasFocus and not self.wasFocus:
        #     self.on_stopFocus()

    def on_startHover(self):    pass#print('start hover')
    def on_hovering(self):      pass#print('hovering')
    def on_stopHover(self):     pass#print('stop hover')
    def on_startClick(self):    pass#print('start click')
    def on_clicking(self):      pass#print('clicking')
    def on_stopClick(self):     pass#print('stop click')
    def on_stopFocus(self):     pass#print('stop focus')
    def on_stopDrag(self):      pass#print('stop focus')

    def on_startDrag(self):
        # print('start drag')
        # TODO: Handle in-place rotation, parent moving,...
        self.clickDelta = self.transf.g_pos - Mouse.pos

    def on_dragging(self):
        #print('dragging')
        #print(self.transf.parent.go.name)
        self.transf.pos = Mouse.pos + self.clickDelta