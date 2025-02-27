from .header_objects import *

# class DragArrow:
#     '''Mũi tên kéo cho IRectEditor'''
#     def __init__(self, idleColor: tuple[int, int, int], width = 4, tipSize = 10.0):
#         self.idleColor = idleColor
#         self.width = width
#         self.tipSize = tipSize

#     @abstractmethod
#     def click_update(self):
#         pass

#     @abstractmethod
#     def render_update(self):
#         pass

class IRectEditor(Interface):
    '''Interface cho di chuyển vật trong chế độ Editor'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uv_coords = (vec(ZERO), vec(ZERO))

        self.draggingId = 0
        self.m_lastpos = vec(ZERO)

    def render_update(self):
        if not mouse.clicked and mouse.host is self:
            self.draggingId = 0
            mouse.host = None
        
        globalMode = pg.key.get_pressed()[pg.K_LSHIFT]
        self.dragArrow(1, colormap['forward'], vec(1, 0), 50, relative=not globalMode)
        self.dragArrow(2, colormap['upward'],  vec(0, 1), 50, relative=not globalMode)
        self.dragArrow(3, colormap['freedom'], vec(1, 1), 30, relative=not globalMode,
                       tipSize=15, freedom=True, showAxis=False, width=6)

        if self.tf.parent:
            self.dragArrow(4, colormap['relation'], vec(0, 0), 0, dest=self.tf.parent.pos,
                           relative=False, width=3, dotted=True)

        pg.draw.circle(screen, colormap['pivot'], self.tf.pos, 4)

    def click_update(self):
        pass        


    def is_mouseInHitbox(self, delta: vec, length: float, width = 5.0, relative = True):
        '''Dùng trick lỏ là quay, khắc chế trục xong quay ngược lại để kiểm bằng dấu <='''
        if mouse.host and mouse.host is not self:
            return False
    
        rel = (mouse.pos - self.tf.pos)
        angle = delta.angle_to((0, 0))
        rel.rotate_ip(angle - relative * self.tf.rot)

        return (-width <= rel.x <= length + width) and \
               (-width <= rel.y <= width)


    def do_dragging(self, id: int, forward: vec, freedom: bool = False, relative = True):
        '''Xử lí việc kéo thả'''
        if not self.draggingId:
            mouse.host = self
            self.draggingId = id
            self.m_lastpos = vec(mouse.pos)
            
        m_dist = mouse.pos - self.m_lastpos
        self.m_lastpos = vec(mouse.pos)
        
        if not freedom: # Kéo có hướng
            angle = forward.angle_to((0, 0))
            delta = m_dist.rotate(-self.tf.rot * relative + angle).elementwise() * vec(1, 0)
            delta.rotate_ip(self.tf.rot * relative - angle)
            self.tf.pos += delta
        else:
            self.tf.pos += m_dist


    def dragArrow(self, id: int, idleColor: tuple[int, int, int], normal: vec, length: float, dest: No[vec] = None,
                  width = 4, tipSize = 10.0, relative = True, freedom = False, showAxis = True, dotted = False):
        '''Vẽ mũi tên kéo và trả về nếu đang kéo'''
        
        if dest:
            delta = dest - self.tf.pos
            normal = delta.normalize()
            length = delta.magnitude()
            tip = normal * tipSize
        else:
            delta = normal * length
            tip = normal * tipSize

        if self.draggingId == 0 and self.is_mouseInHitbox(delta, length, width * 2, relative):
            mouse.host = self
            canStart = True
        else:
            canStart = False

        if self.draggingId == id or canStart:
            color = colormap['white']
            if mouse.clicked:
                self.do_dragging(id, normal, freedom, relative)
                if showAxis:
                    n2 = normal.rotate(self.tf.rot) if relative else normal
                    pg.draw.line(screen, colormap['light'], 
                                 self.tf.pos - n2 * 300, self.tf.pos + n2 * 300)
        else:
            color = idleColor

        if dest:
            delta = dest - self.tf.pos
        
        arrow = [delta, delta + tip.rotate(140), delta + tip.rotate(-140)]
        arrow = [self.tf.pos + dx.rotate(relative * self.tf.rot) for dx in arrow]

        if dotted:
            pos = self.tf.pos.copy()
            dir = (arrow[0] - self.tf.pos).normalize()
            for _ in range(0, int(length), 15):
                pg.draw.line(screen, color, pos, pos + dir * 5, width)
                pos += dir * 15
        else:
            pg.draw.line(screen, color, self.tf.pos, arrow[0], width)

        pg.draw.line(screen, color, arrow[0], arrow[1], width)
        pg.draw.line(screen, color, arrow[0], arrow[2], width)