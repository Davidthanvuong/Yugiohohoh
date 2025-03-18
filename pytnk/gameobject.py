from .engine import *

TCom = TypeVar("TCom", bound="Component")


class Component:
    def _binding(self, go: 'GameObject'):
        if not isinstance(self, Transform): # Tự nó reference chính nó :skull_emoji:
            self.transf = go.transf
        self.go = go
        self.activated = True
        self.after_init()

    def build(self, **kw):
        return GameObject(**kw) + self
        
    def after_init(self): pass
    def update_logic(self): pass
    def update_click(self): pass
    def update_render(self): pass



class Transform(Component):
    def __init__(self, pos: tff = ZERO, anchor: tff = CENTER, rot = 0.0, scale = 1, 
                 hitbox: tff = ZERO, enable_rotation = True, enable_scale = True):
        self.pos = vec(pos)
        self.rot = rot
        self.scale = vec(scale)
        self.anchor = vec(anchor)
        
        self.enable_rotation = enable_rotation
        self.enable_scale = enable_scale
    
        self.hitbox = vec(hitbox)
        #self.l_hitboxTopleft = vec(ZERO)
        self.g_pos = vec(pos)
        self.g_rot = rot
        self.g_scale = vec(scale)

    def after_init(self):
        self.parent = self.go.parent.transf if self.go.parent else None

    def update_logic(self):
        if self.parent is None:
            self.g_pos = self.pos
            self.g_rot = self.rot
            self.g_scale = self.scale
            return
        
        if self.enable_scale:
            self.g_scale = self.scale.elementwise() * self.parent.g_scale
        else: self.g_scale = vONE

        rel = self.pos.elementwise() * self.parent.g_scale
        if self.enable_rotation:
            self.g_rot = self.rot + self.parent.g_rot
            rel.rotate_ip(-self.parent.g_rot)
        else: self.g_rot = 0
        
        self.g_pos = self.parent.g_pos + rel



class GameObject:
    '''GameObject dùng để chạy các components, hoạt động như Unity'''
    root: 'GameObject' = None # type: ignore
    parents_stack: list['GameObject'] = []

    @classmethod
    def get_defaultParent(cls):
        return cls.parents_stack[-1] if len(cls.parents_stack) > 0 else cls.root

    def __init__(self, name: str = "", parent: No['GameObject'] = None, startEnabled = True, **kw):
        self.name = name if name != "" else f"Object {id(self)}"
        self.childs: list['GameObject'] = []
        self.coms: dict[type[Component], Component] = {}

        if not parent: parent = GameObject.get_defaultParent()
        self.parent = parent

        if GameObject.root is None: # Chỉ chạy 1 lần duy nhất
            GameObject.root = self
        else: parent.childs.append(self)

        self.transf: 'Transform'
        self.transf = self.addComponent(Transform(**kw))
        self.enabled = startEnabled

    def __add__(self, com: Component) -> 'GameObject':
        if not self.tryGetComponent(type(com)):
            self.coms[type(com)] = com
            com._binding(self)
        return self

    def __iadd__(self, com: Component) -> 'GameObject':
        return self + com

    def scope(self):
        '''Đặt GameObject vào parent stack để để tạm thời'''
        GameObject.parents_stack.append(self)
        return self

    def unscope(self):
        '''Thu hạm parent stack lại. Để báo lỗi do rỗng luôn cho vui :))'''
        stk = GameObject.parents_stack
        while stk[-1] != self:
            stk.pop()
        stk.pop()
        return self

    def addComponent(self, com: TCom) -> TCom:
        self += com
        return com

    def getComponent(self, com: type[TCom]) -> TCom:
        return self.coms[com] # type: ignore

    def tryGetComponent(self, com: type[TCom]) -> TCom | None:
        '''Bạn sợ à?'''
        return self.coms.get(com, None) # type: ignore
    
    def tryGetParentComponent(self, com: type[TCom]) -> TCom | None:
        '''Tìm component từ parent'''
        return self.parent.tryGetComponent(com) if self.parent else None

    def removeParent(self, reroot = True) -> int:
        if self.parent:
            index = self.parent.childs.index(self)
            self.parent.removeChildren(self, reroot)
            return index
        return -1

    def insertChildren(self, go: 'GameObject', index = -1):
        '''Nhận nuôi GameObject, kết nối parent <---> children'''
        if index == -1: self.childs.append(go)
        else: self.childs.insert(index, go)
        go.parent = self
        go.transf.parent = self.transf

    def removeChildren(self, go: 'GameObject', reroot = True):
        '''Jack bỏ con'''
        self.childs.remove(go)
        if reroot: GameObject.root.insertChildren(go)

    def update_logic(self):
        for com in list(self.coms.values()):
            if com.activated: com.update_logic()

        for child in self.childs:
            if child.enabled: child.update_logic()

    def update_click(self):
        for com in list(reversed(self.coms.values())):
            if com.activated: com.update_click()

        for child in reversed(self.childs):
            if child.enabled: child.update_click()

    def update_render(self):
        for com in list(self.coms.values()):
            if com.activated: com.update_render()

        for child in self.childs:
            if child.enabled: child.update_render()

    def destroy(self):
        if self.parent:
            self.parent.childs.remove(self)
        # self.enabled = False # Test GC