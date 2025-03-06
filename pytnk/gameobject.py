import pickle, os
from typing import TypeVar, Type, cast
from copy import deepcopy
from .header_pygame import *

T = TypeVar("T", bound="Component")


class Component:    
    '''Class để chạy các chức năng từ vật'''

    def __init__(self, go: No['GameObject'] = None):
        if go: 
            self.go = go
            self.go.coms[self.__class__.mro()[0]] = self
        else: self.go: 'GameObject'


    def update_logic(self): pass
    def update_click(self): pass
    def update_render(self): pass

    @staticmethod
    def create_default() -> 'GameObject': 
        raise Exception("Not implemented")
    # Tạo gameobject mẫu từ Component
    # (Tốt cho singletons)

    # def __init__(self, bind: 'Transform'):
    #     self.tf = bind
    #     bind.coms[self.__class__.mro()[0]] = self # mro đầu tên là đời con xa nhất




class GameObject:
    '''GameObject hỗ trợ Components như Unity
    \n✅ Các components cần thiết cho vật: Collider, Image, Text
    \n✅ Các hàm cần thiết cho vật
    \n🟨 Render + position system bám vào anchor
    '''

    PrefabPath = "assets\\prefabs\\{}"
    Prefabs: dict[str, 'GameObject'] = {}
    # TODO: Lookup: dict[str, 'GameObject'] = {}


    e_onCreateGO: Event['GameObject'] = Event()
    e_onChangedChilds: Event['GameObject'] = Event()


    def __init__(self, name = "", pos: tff = ZERO, pivot: tff = TOPLEFT, anchor: No[tff] = None, rot = 0.0, scale: tff = ONE, 
                 hitbox: tff = ZERO, indent = 0, parent: No['GameObject'] = None, fit: tuple[bool, bool] = (False, False),
                 sceneName = "", createScene = False, enabled = True, simple = False):
        self.name = name if name != "" else f"Object {id(self)}"
        self.parent = parent
        self.childs: list['GameObject'] = []
        self.coms: dict[type['Component'], 'Component'] = {}

        self.pos = vec(pos) # Integrate trực tiếp Transform vào GameObject
        self.rot = rot
        self.scale = vec(scale)
        self.pivot = vec(pivot)
        self.anchor = vec(anchor) if anchor else None # Bám theo hitbox của parent, không có thì thôi
        self.hitbox = vec(hitbox)
        self.indent = indent
        self.parent = parent
        self.fit = fit
        
        self.global_pos = vec(pos)
        self.global_rot = rot
        self.global_scale = vec(scale)

        if self.parent: 
            self.parent.childs.append(self)

        if createScene: # WTF move to getScene function
            self.sceneName = name
            self.scene = Window.Scenes[self.name] = Scene(self, pg.Surface(hitbox, pg.SRCALPHA))
        elif sceneName != "":
            self.sceneName = sceneName
            self.scene = Window.Scenes[sceneName]
        elif self.parent:
            self.sceneName = self.parent.sceneName
            self.scene = self.parent.scene
        else:
            self.sceneName = 'Maingame'
            self.scene = Window.Scenes['Maingame']
            self.parent = self.scene.go
            self.scene.go.addChildren(self)
            # Không tìm thấy thì đặt mặt định maingame
        
        self.createScene = createScene
        self.enabled = enabled
        self.simple = simple        # Giản lược chức năng xoay
        self.scope = Scope()
        self.exist = True

        GameObject.e_onCreateGO(self)

    
    def __call__(self, pos: tff = ZERO):
        self.pos = vec(pos)


    def __add__(self, com: type[T] | Component) -> 'GameObject':
        '''Tạo liên tiếp các components'''
        if isinstance(com, type):
            if not self.existComponent(com):
                obj = com(self)
                self.coms[com] = obj
        elif isinstance(com, Component):
            if not self.existComponent(type(com)):
                com.go = self
                self.coms[type(com)] = com
        return self

    
    def __iadd__(self, com: type[T] | Component) -> 'GameObject':
        return self + com


    def addComponent(self, com: type[T]) -> T:
        obj = com(go=self)
        return obj
    

    def getComponent(self, com: type[T]) -> T:
        return cast(T, self.coms[com])


    def existComponent(self, com: type[T]) -> bool:
        '''Bạn sợ à?'''
        return com in self.coms
    

    def addChildren(self, go: 'GameObject'):
        '''Nhận nuôi GameObject, kết nối parent <---> children'''
        self.childs.append(go)
        GameObject.e_onChangedChilds(self)
        go.parent = self
        

    def update_logic(self):
        if not self.enabled: return
        for com in self.coms.values():
            com.update_logic()
        self.update_global()

        for child in self.childs:
            child.update_logic()


    def update_click(self):
        if not self.enabled: return
        for com in reversed(self.coms.values()):
            com.update_click()

        for child in reversed(self.childs):
            child.update_click()


    def update_render(self):
        if not self.enabled: return
        for com in self.coms.values():
            com.update_render()

        self.scene.gizmos_rect(Color.freedom, self.scope, -2)

        for child in self.childs:
            child.update_render()
            self.scope.update(child.scope)
            
        self.scene.gizmos_rect(Color.white, self.scope, -4)


    def update_global(self):
        '''Cập nhật tính chất global của vật (chạy mỗi frame sau logic)'''
        if not self.parent:
            # Chỉ chạy khi vật là scene (gốc của mọi vật)
            self.global_scale = self.scale
            self.global_rot = self.rot
            self.global_pos = self.pos
            if self.fit[0]: self.hitbox.x = Window.native[0]
            if self.fit[1]: self.hitbox.y = Window.native[1]
            if self.createScene:
                self.scene.buffer = pg.transform.scale(self.scene.buffer, self.hitbox)
            if self.anchor:
                amount = ((Window.native - self.hitbox).elementwise() * self.anchor).elementwise() * self.global_scale
                self.global_pos = self.pos + amount
        else:
            self.global_scale = self.scale.elementwise() * self.parent.global_scale
            self.global_rot = self.rot + self.parent.global_rot
            rel = self.pos.elementwise() * self.parent.global_scale
            if self.fit[0]: self.hitbox.x = self.parent.hitbox.x
            if self.fit[1]: self.hitbox.y = self.parent.hitbox.y
            if self.anchor:
                rel += ((self.parent.hitbox - self.hitbox).elementwise() * self.anchor).elementwise() * self.global_scale
            if not self.simple:
                rel.rotate_ip(self.parent.global_rot)
            
            self.global_pos = self.parent.global_pos + rel


    @classmethod
    def existPrefab(cls, name: str, store = True) -> bool:
        '''Thử xem tồn tại hay không, thường dùng trong việc generate prefab'''
        if store and cls.Prefabs.get(name):
            return True
 
        path = f"assets\\prefabs\\{name}"
        return os.path.exists(path)
    

    @classmethod
    def getPrefab(cls, name: str, store = True) -> 'GameObject':
        '''Chép hoàn toàn prefab từ bộ nhớ (store), không có thì thử mở'''
        obj = cls.Prefabs.get(name) if store else None
 
        path = cls.PrefabPath % name
        if not obj and os.path.exists(path):
            with open(path, "rb") as f:
                obj = pickle.load(f)
                if store: cls.Prefabs[name] = obj

        deep = deepcopy(cast('GameObject', obj))
        deep.name += f" ({id(deep)})"
        return deep


    def saveSelf(self, name: str = "", delete = False):
        '''Lưu prefab vào assets/prefab'''
        path = GameObject.PrefabPath % (name if name != "" else self.name)
        os.makedirs("assets\\prefabs\\", exist_ok=True)

        with open(path, "wb") as f:
            pickle.dump(self, f)
        
        if delete and self.parent: 
            self.parent.childs.remove(self) # Let GC cook

        print(f"Đã lưu {path}")


    def __getstate__(self):
        '''Lưu vật đến pickle'''
        state = self.__dict__.copy()
        state.pop("scene", None)        # Không thể serialize con trỏ
        return state
    

    def __setstate__(self, state):
        '''Đọc vật từ pickle'''
        self.__dict__.update(state)
        self.scene = Window.Scenes[self.sceneName]