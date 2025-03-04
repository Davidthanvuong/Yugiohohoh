import pickle, os
from typing import TypeVar, cast, Any
from random import randint as rint
from copy import deepcopy
from .header_pygame import *


T = TypeVar("T", bound="Component")
rootT = tuple['Transform', pg.Surface]


class Transform:
    '''Class quốc dân'''
    prefabs: dict[str, 'Transform'] = {}
    roots: dict[str, rootT] = {} # Maingame là mặc định

    def __init__(self, name: str = "", pos: tff = ZERO, pivot: tff = TOPLEFT, hitbox: tff = ZERO, parent: No['Transform'] = None,
                 angle = 0.0, scale: tff = ONE, enabled = True, no_angle = False, rootname: str = ""):
        self.name = name if name != "" else f"Object {id(self)}"
        self.pos = vec(pos)
        self.angle = angle
        self.scale = vec(scale)
        self.pivot = vec(pivot)
        self.parent = parent
        self.hitbox = vec(hitbox)
        
        if parent: parent.adoptChildren(self)
        if rootname == "" and parent and parent.root is not None:
            self.rootname = parent.rootname
            self.root = parent.root
        else:
            self.rootname = rootname
            self.root = Transform.roots.get(rootname, (self, pg.Surface(ZERO)))
        
        self.childrens: list['Transform'] = []
        self.coms: dict[type['Component'], 'Component'] = {}

        self.no_angle = no_angle # Tắt xoay
        self.enabled = enabled

        self.global_pos = vec(pos)
        self.global_angle = angle
        self.global_scale = vec(scale)


    def update_logic(self):
        if not self.enabled: return
        for com in self.coms.values():
            com.update_logic()
        self.update_global()

        for child in self.childrens:
            child.update_logic()


    def update_click(self):
        if not self.enabled: return
        for com in reversed(self.coms.values()):
            com.update_click()

        for child in reversed(self.childrens):
            child.update_click()


    def update_render(self):
        if not self.enabled: return
        for com in self.coms.values():
            com.update_render()

        for child in self.childrens:
            child.update_render()


    def update_global(self):
        '''Cập nhật tính chất global của vật (chạy mỗi frame sau logic)'''
        if not self.parent:
            self.global_scale = self.scale
            self.global_angle = self.angle
            self.global_pos = self.pos
        else:
            self.global_scale = self.scale.elementwise() * self.parent.global_scale
            self.global_angle = self.angle + self.parent.global_angle
            rel = self.pos.elementwise() * self.parent.global_scale
            if not self.no_angle:
                rel.rotate_ip(self.parent.global_angle)
            
            self.global_pos = self.parent.global_pos + rel


    def collidepoint(self, pos: vec): #todo
        pass


    def collidetf(self, tf: 'Transform'):
        pass


    # def addComponent(self, com: type[T]) -> T:
    #     '''Tạo component clean nhất, nhớ start'''
    #     obj = com(self)
    #     self.coms[com] = obj
    #     return obj

    
    def getComponent(self, com: type[T]) -> T:
        '''Lấy component đúng cách'''
        return cast(T, self.coms[com])
    

    def tryComponent(self, com: type[T]) -> T | None:
        '''Bạn sợ à?'''
        t = self.coms.get(com)
        return cast(T, t) if t else None
    

    def adoptChildren(self, tf: 'Transform'):
        '''Nhận nuôi transform, kết nối parent <---> children'''
        self.childrens.append(tf)
        tf.parent = self
        

    @staticmethod
    def existPrefab(name: str, store = True) -> bool:
        '''Thử xem tồn tại hay không, thường dùng trong việc generate prefab'''
        if store and Transform.prefabs.get(name):
            return True
 
        path = f"assets\\prefabs\\{name}"
        return os.path.exists(path)
    

    @staticmethod
    def getPrefab(name: str, parent: No['Transform'] = None, pos: No[vec] = None, store = True) -> 'Transform':
        '''Chép hoàn toàn prefab từ bộ nhớ (store), không có thì thử mở'''
        obj = Transform.prefabs.get(name) if store else None
 
        path = f"assets\\prefabs\\{name}"
        if not obj and os.path.exists(path):
            with open(path, "rb") as f:
                obj = pickle.load(f)
                if store: Transform.prefabs[name] = obj

        #assert obj is None
        deep = deepcopy(cast('Transform', obj))
        if parent: parent.adoptChildren(deep)
        if pos: deep.pos = pos
        deep.name += f" ({id(deep)})"
        print(f"Tạo thành công {deep.name}")
        return deep


    def saveSelf(self, name: str = "", delete = False):
        '''Lưu prefab vào assets/prefab'''
        path = f"assets\\prefabs\\{name if name != '' else self.name}"
        old_parent = self.parent # Không lưu parent ngoài
        if self.parent:
            self.parent.childrens.remove(self)
        self.parent = None
        
        os.makedirs("assets\\prefabs\\", exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        
        if not delete: self.parent = old_parent # Let GC cook
        print(f"Saved {path}")



    def __getstate__(self):
        '''Lưu vật đến pickle'''
        state = self.__dict__.copy()
        state.pop("root", None)        # Không thể serialize con trỏ
        return state
    

    def __setstate__(self, state):
        '''Đọc vật từ pickle'''
        self.__dict__.update(state)
        
        if (self.rootname == "") and (self.parent) and (self.parent.root is not None):
            self.rootname = self.parent.rootname
            self.root = self.parent.root
        else:
            self.rootname = self.rootname
            self.root = Transform.roots.get(self.rootname, (self, pg.Surface(ZERO)))



class Component:    
    '''Class để chạy các chức năng từ vật (Transform)'''

    def __init__(self, bind: 'Transform'):
        self.tf = bind
        bind.coms[self.__class__.mro()[0]] = self # mro đầu tên là đời con xa nhất
    # @classmethod
    # def get_defaultKeys(cls) -> dict[str, Any]:
    #     """Lấy từ MRO các `Component`"""
    #     keys = {}
    #     for base in reversed(cls.__mro__):
    #         keys.update({
    #             key: value for key, value in base.__dict__.items()
    #             # Loại các static (ghi in) và hàm ra, còn lại trôm hết
    #             if (not key[0].isupper()) and (not callable(value))
    #         })
    #     return keys


    # def __init__(self, tf: 'Transform'):
    #     self.tf = tf
    #     for key, value in self.get_defaultKeys().items():
    #         setattr(self, key, value)

    # def __call__(self, **kwargs): pass
    def update_logic(self): pass
    def update_click(self): pass
    def update_render(self): pass